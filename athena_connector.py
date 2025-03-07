import time
import boto3
import pandas as pd
import io

class QueryAthena:
    
    def __init__(self, query, database, timeout=1):
        self.database = database       
        self.timeout= timeout       
        self.query = query
        
    def load_conf(self, q):
        try:
            self.client = boto3.client('athena')
            response = self.client.start_query_execution(
                QueryString = q,
                    QueryExecutionContext={
                    'Database': self.database
                    }                  
            )
            self.filename = response['QueryExecutionId']
            print('Execution ID: ' + response['QueryExecutionId'])
            print(response)
            return response

        except Exception as e:
            print(e)                
  
    def run_query(self):
        queries = [self.query]
        for q in queries:
            res = self.load_conf(q)
        try:              
            query_status = None
            response = None
            while query_status == 'QUEUED' or query_status == 'RUNNING' or query_status is None:
                response = self.client.get_query_execution(QueryExecutionId=res["QueryExecutionId"])
                
                query_status = response['QueryExecution']['Status']['State']               
                if query_status == 'FAILED' or query_status == 'CANCELLED':
                    raise Exception('Athena query with the string "{}" failed or was cancelled'.format(self.query))
                time.sleep(self.timeout)
            print('Query "{}" finished.'.format(self.query))
            print(response)
            self.s3_output_path = response['QueryExecution']['ResultConfiguration']['OutputLocation']
            df = self.obtain_data()
            return df
            
        except Exception as e:
            print(e)      
            
    def obtain_data(self):
        try:
            self.resource = boto3.resource('s3')
            bucket = self.s3_output_path.split("/")[2]
            key = self.s3_output_path.replace("s3://" + bucket + "/", "")
            response = self.resource \
            .Bucket(bucket) \
            .Object(key= key) \
            .get()
            print(response)
            return pd.read_csv(io.BytesIO(response['Body'].read()), encoding='utf8')   
        except Exception as e:
            print(e)  
# query = 'SELECT * FROM "edw"."ar_adjustments_dim" order by create_dt limit 10;'
# qa = QueryAthena(query=query, database='edw')
# dataframe = qa.run_query()
# dataframe

# job.commit()