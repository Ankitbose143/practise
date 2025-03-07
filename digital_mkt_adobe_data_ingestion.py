# %extra_py_files s3://cci-edo-data-utils/alteryx_digital_marketing/adobe_config_read.py
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import aanalytics2 as api2
from authlib.integrations.requests_client import OAuth2Session
import requests
import datetime
import time
import pandas as pd
import json
from adobe_config_read import QueryAthena
import ast
import boto3
import io
from datetime import timedelta
import boto3
from botocore.exceptions import ClientError
 

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

database_name_arg = getResolvedOptions(sys.argv, ['database_name'])
database_name =database_name_arg['database_name']
    

def timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')       


class AdobeAnalysticsQueryExecutor():

    POST_RQ_STEP1 = 'https://api5.omniture.com/admin/1.4/rest/?method=Report.Queue'
    POST_RG_STEP2 = 'https://api5.omniture.com/admin/1.4/rest/?method=Report.Get'

    def __init__(self, client_id, client_secret, token_endpoint, scopes, org_id):
        self.org_id = org_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint = token_endpoint
        self.scopes = scopes
        self.cids = None
        self.suites = None
        self.rsid = None
        self.params = None
        self.r1 = None
        self.r2 = None
        self.df = None
        self.cols = None

   
        
    def __raise_login_error(self):
        if self.adobe_client is None:
            raise ("Login is required")


    def try_with_backoff(self, payload):
        print(f'{timestamp()} trying request')
        req = requests.post(url=self.POST_RG_STEP2,
                            headers=self.headers, json=payload)
        n = 1
        while (req.status_code != 200) and (n<=5):  # and (n<=5):
        
            print(
                f'{timestamp()} req.status = {req.status_code} -- sleep for {10} secs Retry count {n}')
            time.sleep(10)
            
            print(f'{timestamp()} retry request with payload {payload} ')
            try:
                req = requests.post(url=self.POST_RG_STEP2,
                                headers=self.headers, json=payload)
            except Exception as e:
                print(e)
            n += 1
        if (req.status_code != 200):
            print(f'error -- {req.text}')
            return f'error -- {req.text}'

        return req.json()
        
        
    def login(self):
        oauth = OAuth2Session(
            self.client_id, self.client_secret, scope=self.scopes)
        self.token = oauth.fetch_token(self.token_endpoint)["access_token"]
        api2.configure(oauth=True, org_id=self.org_id,
                       client_id=self.client_id, token=self.token)
        self.adobe_client = api2.Login()
        self.__raise_login_error()
        self.cids = self.adobe_client.getCompanyId()
        self.mycompany = api2.Analytics(self.cids[0]["globalCompanyId"])
        self.suites = self.mycompany.getReportSuites()
        self.rsid = self.suites[self.suites["name"]
                                == "Avalanche Prod"]["rsid"]
        self.rsid = self.rsid.reset_index()["rsid"][0]
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}',
            'x-api-key': self.client_id,
            'x-proxy-global-company-id': self.mycompany.company_id,
        }
        print("Generated Adobe API Tokens Sucessfully")
        return [self.rsid,self.headers]

    def flatmap_aanalytics_report(self, data, vals=[], output=[]):
        for row in data:
            if "name" in row:
                vals.append(row["name"])
                if "breakdown" in row:
                    self.flatmap_aanalytics_report(
                        row["breakdown"], vals, output)
                elif "counts" in row:
                    output.append(vals + row["counts"])
                vals.pop()
        return output
        
    def execute_get_report(self,query, s3_output_path):
        spark_df = None
        print(f"Starting get report query for payload {query}")
        r1 = requests.post(url=self.POST_RQ_STEP1,
                           headers=self.headers, json=query)
        print(r1.text)
        if r1.status_code != 200:
            raise Exception(r1.text)
        print("Waiting on Queue to complete Report generation of: " + r1.text)
        r2 = self.try_with_backoff(r1.json())  
        report_output = self.flatmap_aanalytics_report(r2["report"]["data"],[],[])
        cols = ["date"]
        if len(query["reportDescription"]["elements"])>0:
            cols += [row["name"] for row in r2["report"]["elements"]]
        
        cols += [row["name"] for row in r2["report"]["metrics"]]
        if len(report_output) == 0:
            return 0
        df = pd.DataFrame(report_output, columns=cols)
        report_output=[]
        r2=[]
        
        
        spark_df = spark.createDataFrame(df)
        spark_df.write.mode("overwrite").parquet(s3_output_path)
        print(f"row count for adobe query is {len(df)}")
        print(f"Completed get report query for payload {query} and uploaded to {s3_output_path}")
        df = None
        return spark_df.count()

def publish_to_sns(subject:str, message:str, sns_arn:str):
            
            try:
               SNS_CLIENT = boto3.client("sns")
               SNS_CLIENT.publish(
                   TopicArn=sns_arn,
                   Message=message,
                   Subject=subject,
               )
            except Exception as e:
                print(e)
                raise e
               
               
               

def run_process(metadata, adobe_client,log_time,retry=False,retry_cnt = 0):
    try:
        if retry:
            update_config_pquery = f"""
                    update  {database_name}.digital_mkt_process_config  set job_status='InProgress', last_upt_dt=TIMESTAMP '{timestamp()}' where process_id = '{metadata["process_id"]}'
            """
            update_config_rquery = QueryAthena(query=update_config_pquery, database=database_name)
            update_config_rquery.run_query(False)
        else:
            insert_log_pquery = f"""
                        INSERT INTO {database_name}.digital_mkt_process_auditlog  
                        (process_id, job_id, job_nm, process_nm, process_status, process_start_dt, process_end_dt,retry_count,records_processed) 
                        VALUES ('{metadata["process_id"]}', {metadata["job_id"]}, '{metadata["job_nm"]}', '{metadata["process_nm"]}', 'InProgress',TIMESTAMP '{log_time}', NULL,{retry_cnt},0)
                    """
            
            insert_log_progress = QueryAthena(query=insert_log_pquery, database=database_name)
            insert_log_progress.run_query(False)
           
        adobe_payload = json.loads(metadata["input_config_json"])
        adobe_payload["reportDescription"]["dateFrom"]=( datetime.datetime.now() -timedelta(days=int(adobe_payload["reportDescription"]["dateFrom"]))).strftime('%Y-%m-%d')
        print("start date is "+ adobe_payload["reportDescription"]["dateFrom"])
        adobe_payload["reportDescription"]["dateTo"]= ( datetime.datetime.now() -timedelta(days=int(adobe_payload["reportDescription"]["dateTo"]))).strftime('%Y-%m-%d')
        print(f"end date is "+adobe_payload["reportDescription"]["dateTo"])
        s3_location = json.loads(metadata["output_config_json"])
        row_count = adobe_client.execute_get_report(adobe_payload,s3_location["s3_location"])
        
        print(f"the row count of adobe data is {row_count}")
        if row_count==0 and  metadata["process_id"] not in ['2900-1','1300-4','2400-10']:
            print(f"the row count of adobe data is {row_count}")
            print("Failed to execute the process : " + metadata["process_id"])
            up_config_query =f""" update  {database_name}.digital_mkt_process_config  set job_status='Failed', last_upt_dt=TIMESTAMP '{timestamp()}' where process_id = '{metadata["process_id"]}'  """
            up_qa = QueryAthena(query=up_config_query, database=database_name)
            up_qa.run_query(False)
            
            update_log_fquery = f"""
                        update {database_name}.digital_mkt_process_auditlog 
                        set process_status = 'Failed', process_end_dt = TIMESTAMP '{timestamp()}', retry_count={retry_cnt}, records_processed = 0  where process_id ='{metadata["process_id"]}' and process_start_dt = TIMESTAMP '{log_time}'
                    """
            update_log_failed = QueryAthena(query=update_log_fquery, database=database_name)
            update_log_failed.run_query(False)
            return False

            
        
            
        print("Fetched the Adobe analytics output for processId: " + metadata["process_id"])
        job_output.append({
            "processId" : metadata["process_id"],
            "status" : "success"
        })
        up_config_query =f""" update  {database_name}.digital_mkt_process_config  set job_status='Success', last_upt_dt=TIMESTAMP '{timestamp()}' where process_id = '{metadata["process_id"]}'  """
        up_qa = QueryAthena(query=up_config_query, database=database_name)
        up_qa.run_query(False)
        update_log_squery = f"""
                    update {database_name}.digital_mkt_process_auditlog 
                    set process_status = 'Success', process_end_dt = TIMESTAMP '{timestamp()}', retry_count={retry_cnt} , records_processed = {row_count}  where process_id ='{metadata["process_id"]}' and process_start_dt = TIMESTAMP '{log_time}'
                """
        update_log_success = QueryAthena(query=update_log_squery, database=database_name)
        update_log_success.run_query(False)
        row_count = 0
        return True
    except Exception as err:
        print(err)
        print("Failed to execute the process : " + metadata["process_id"])
        up_config_query =f""" update  {database_name}.digital_mkt_process_config  set job_status='Failed', last_upt_dt=TIMESTAMP '{timestamp()}' where process_id = '{metadata["process_id"]}'  """
        up_qa = QueryAthena(query=up_config_query, database=database_name)
        up_qa.run_query(False)
        
        update_log_fquery = f"""
                    update {database_name}.digital_mkt_process_auditlog 
                    set process_status = 'Failed', process_end_dt = TIMESTAMP '{timestamp()}', retry_count={retry_cnt}, records_processed = 0  where process_id ='{metadata["process_id"]}' and process_start_dt = TIMESTAMP '{log_time}'
                """
        update_log_failed = QueryAthena(query=update_log_fquery, database=database_name)
        update_log_failed.run_query(False)
        return False


def get_secret(id_name):
 
 
    region_name = "us-east-1"
 
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
 
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=id_name
        )
    except ClientError as e:
        raise e
 
    secret = json.loads(get_secret_value_response['SecretString'])
    return secret

if __name__ == "__main__":
    
    secret_arg = getResolvedOptions(sys.argv, ['secret_name'])
    secret_name =secret_arg['secret_name']
    
    sns_arn_arg = getResolvedOptions(sys.argv, ['sns_arn'])
    sns_arn =sns_arn_arg['sns_arn']
    
    secret = get_secret(secret_name)
    my_org_id = secret["my_org_id"]
    my_token_endpoint = secret["my_token_endpoint"]
    my_client_secret = secret["my_client_secret"]
    my_client_id = secret["my_client_id"]
    
    scopes = "openid, AdobeID, additional_info.projectedProductContext"
    args = getResolvedOptions(sys.argv, ['process_id_list'])
    process_id_list = args['process_id_list'].split(',')
    print(process_id_list)
    # api = AdobeAnalysticsQueryExecutor(my_client_id, my_client_secret, my_token_endpoint, scopes, my_org_id)
    # api.login()
    process_count = 0
    job_name  = None
    job_output = []
    failed_process_id = {}
    database_name_arg = getResolvedOptions(sys.argv, ['database_name'])
    database_name =database_name_arg['database_name']
    
    bucket_name_arg = getResolvedOptions(sys.argv, ['bucket_name'])
    bucket_name =bucket_name_arg['bucket_name']
    
    path_arg = getResolvedOptions(sys.argv, ['path'])
    path =path_arg['path']
    
    try:
        for i in process_id_list:
            api = AdobeAnalysticsQueryExecutor(my_client_id, my_client_secret, my_token_endpoint, scopes, my_org_id)
            api.login()
            query = f"""select * from {database_name}.digital_mkt_process_config where process_id='{i}'"""
            qa = QueryAthena(query=query, database=database_name)
            metadata = qa.run_query()
            metadata = metadata.iloc[0].to_dict()
            print(f"Received Job metadata : {metadata}")
            job_name = metadata["job_nm"]
            log_time = timestamp()
            print(f"log time : {log_time}")
            status = run_process(metadata, api,log_time)
            if status:
                process_count += 1
            else:
                retry_count = 1
                while retry_count<=3:
                    status = run_process(metadata, api,log_time,True,retry_count)
                    if status:
                        process_count +=1
                        break
                    else:
                        failed_process_id[i]=retry_count
                        print(f"retry count for failed process_id{i} is {retry_count}")
                        retry_count+=1
                        
        print(f"failed_process_id list and retry counts{failed_process_id}")
                        
                
        if process_count == len(process_id_list):
            print("completed all processes")
            filename = str(metadata["job_id"]) + "_" + timestamp() + ".done"
            path = path+"job_id="+str(metadata["job_id"])+"/"
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(bucket_name)
            bucket.upload_fileobj(io.BytesIO(json.dumps(job_output).encode("utf-8")), path + filename)
            print("Sucessfully uploaded job status file for porcesss: " + args['process_id_list'])  
        else:
            print("send mail")
            # sns_arn = "arn:aws:sns:us-east-1:254158912258:digital_mkt_notification"
            subject = f"Failed Adobe API Calls for {job_name}"
            message = f""" Hi Team,
                    Adobe API calls failed for  {job_name} workflow with below process id's 
                    {failed_process_id}
                    Thankyou"""
            
            publish_to_sns(subject, message, sns_arn)
        
                
                
            
    except Exception as err:
        print(err)
        print("Failed adobe job execution for jobs: "  +  args['process_id_list'])




