import json
import boto3
import os
import pymysql
from datetime import datetime

def get_secret(secret_nm):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name='us-east-1')
    get_secret_value_response = client.get_secret_value(SecretId=secret_nm)
    secret = get_secret_value_response['SecretString']
    return secret


def createDBConnection(aurora_credentials):
    try:
        secret = get_secret(aurora_credentials)
        secret = eval(secret)
        return pymysql.connect(host=secret['host'], user=secret['username'], passwd=secret['password'], port=int(secret['port']), db=secret['dbname'], autocommit=True)
    except Exception as err:
        print('Error connecting to RDS:', err)
        raise

def insert_file_log(aurora_credentials, start_date, end_date, file_name, status, error_message):
    conn = createDBConnection(aurora_credentials)
    cursor = conn.cursor()

    query = 'INSERT INTO FILE_LOG_GG (FILE_DEFINITION_ID, FILE_DEFINITION_NM, FILE_PROCESS_STATUS, FILE_DT, CREATE_DT, ERROR_MSG) \
                VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'.format('gg_data_move', file_name, status,
                                                                                 start_date, end_date, error_message)
    print('Query is {}'.format(query))

    try:
        cursor.execute(query)
        print('Successfully executed query')
    except Exception as err:
        print('Cannot execute query:', err)
        raise

def lambda_handler(event, context):
    try:
        aurora_credentials = os.environ['aurora_credentials']

        print(f"event={event}")

        bucket_name = json.loads(event["Records"][0]["body"])["Records"][0]["s3"]["bucket"]["name"]
        object_key = json.loads(event["Records"][0]["body"])["Records"][0]["s3"]["object"]["key"]
        object_time = json.loads(event["Records"][0]["body"])["Records"][0]["eventTime"]
        print(bucket_name)
        print(object_key)

        s3 = boto3.resource('s3')
        copy_source = {
            'Bucket': bucket_name,
            'Key': object_key
        }

        replication_bucket= os.environ['replication_bucket']
        bucket = s3.Bucket(os.environ['replication_bucket'])
        external_bucket = s3.Bucket(os.environ['external_replication_bucket'])
        curated_bucket = s3.Bucket(os.environ['curated_bucket'])
        dio_path = os.environ['dio_replication_path']
        secured_bucket = s3.Bucket(os.environ['secured_bucket'])

        if bucket_name == os.environ['secured_bucket']:
            object_key = object_key.replace("replication/","")
            print("object_key : ", object_key)
        system = object_key.split('/')[1]

        if system == 'pstage':

            try:
                date = object_key.split('/')[3].split('_')[-2]
                month = '-'.join(object_key.split('/')[3].split('_')[-2].split('-')[:-1])
                table = object_key.split('/')[2].split('_')[1]
                site_name = object_key.split('/')[2].split('_')[0]
                new_key = 'curated/' + object_key.split('/')[1] + '/' + table + '/site='+ site_name.lower() + '/dt=' + date.lower() + '/' + object_key.split('/')[-1].replace('.parquet', '_uncompressed.parquet')
                if bucket_name == replication_bucket:
                    bucket.copy(copy_source, new_key)
                else:
                    new_key = 'replication/' + new_key
                    secured_bucket.copy(copy_source, new_key)
                print("{} bucket: {} Object_Key={} Date={} Table={} New_Key={}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), bucket_name, object_key,date,table,new_key))

            except Exception as err:
                print("{} Message='File Process Failed, Please Check The Logs' Error={}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),err))
                err_msg = str(err).replace("'", "").replace('"', '')
                insert_file_log(aurora_credentials, datetime.now(), datetime.now(), 's3://' + bucket_name + '/' + object_key, 'FAILED', err_msg[:2000])


        elif system == 'pinpnt':

            date = object_key.split('/')[4].split('_')[-2]
            table = object_key.split('/')[3]

            new_key = 'curated/pinpoint/' + table + '/dt=' + date.lower() + '/' + object_key.split('/')[-1].replace('.parquet', '_uncompressed.parquet')
            bucket.copy(copy_source, new_key)

        elif system == 'cns_audit':

            date = object_key.split('/')[3].split('_')[-2]
            table = object_key.split('/')[2]

            new_key = 'curated/cns_audit/' + table + '/dt=' + date.lower() + '/' + object_key.split('/')[-1].replace('.parquet', '_uncompressed.parquet')
            bucket.copy(copy_source, new_key)

        elif system == 'payment':

            date = object_key.split('/')[3].split('_')[-2]
            table = object_key.split('/')[2]

            new_key = 'curated/payment/' + table + '/dt=' + date.lower() + '/' + object_key.split('/')[-1].replace('.parquet', '_uncompressed.parquet')
            bucket.copy(copy_source, new_key)

        elif system in ['ods', 'pptnrsvc', 'pprov', 'pvantage', 'pcallctr', 'pcbma', 'oltpshd', 'pgranite', 'pnoi', 'pcustomer', 'prbm']:

            date = object_key.split('/')[4].split('_')[-2]
            table = object_key.split('/')[3]
            schema = object_key.split('/')[2]

            new_key = 'curated/' + system + '/' + schema + '/' + table + '/dt=' + date.lower() + '/' + object_key.split('/')[-1].replace('.parquet', '_uncompressed.parquet')
            bucket.copy(copy_source, new_key)

        elif system == 'xgl':
            date = object_key.split('/')[3].split('_')[-2]
            table = object_key.split('/')[2]

            new_key = 'ap/xgl/' + table + '/dt=' + date.lower() + '/' + object_key.split('/')[-1]
            external_bucket.copy(copy_source, new_key)

        elif system == 'dbo':
            date = object_key.split('/')[3].split('_')[-2]
            table = object_key.split('/')[2]

            new_key = 'curated/dbo/' + table + '/dt=' + date.lower() + '/' + object_key.split('/')[-1].replace('.parquet', '_uncompressed.parquet')
            bucket.copy(copy_source, new_key)

        elif system == 'cmi_biller':
            date = object_key.split('/')[4].split('_')[-2]
            table = object_key.split('/')[3]

            new_key = 'cmi_biller/data/' + table + '/dt=' + date.lower() + '/' + object_key.split('/')[-1]
            print("new_key :",new_key)
            curated_bucket.copy(copy_source, new_key)

        elif system == 'xgl-full':
            date = object_key.split('/')[3].split('_')[-2]
            table = object_key.split('/')[2]

            new_key = 'xgl-full/' + table + '/dt=' + date.lower() + '/' + object_key.split('/')[-1]
            curated_bucket.copy(copy_source, new_key)

        elif system == 'dio':
            table = object_key.split('/')[2]
            time_parts = object_time.split(sep=':')
            creation_date = object_time[0:10].replace('-','')
            creation_time = time_parts[0][11:] + time_parts[1] + time_parts[2][0:6].replace('.','')
            file_name = table + '_' + creation_date + '_' + creation_time + '.parquet'

            new_key = dio_path + table + '/dt=' + object_time[0:10].lower() + '/' + file_name
            external_bucket.copy(copy_source, new_key)

        elif system == 'jacada':
            date = object_key.split('/')[3].split('_')[-2]
            table = object_key.split('/')[2]

            new_key = 'curated/jacada/' + table + '/dt=' + date.lower() + '/' + object_key.split('/')[-1].replace('.parquet', '_uncompressed.parquet')
            bucket.copy(copy_source, new_key)

        ############Raghav Added This Block for FIG Notifications on 08/16/2021
        elif system == "fig":
            try:
                date = object_key.split('/')[3].split('_')[-2] # This would be 'YYYY-mm-dd'
                table = object_key.split('/')[2]  # This would be 'notifications'
                new_key = 'curated/fig/' + table + '/dt=' + date.lower() + '/' +object_key.split('/')[-1].replace('.parquet', '_uncompressed.parquet') #This would be File Name
                bucket.copy(copy_source, new_key)
                print("{} bucket_name = {} Object_Key={} Date={} Table={} New_Key={}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),bucket_name,object_key,date,table,new_key))
            except Exception as err:
                print("{} Message='File Process Failed, Please Check The Logs' Error={}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),err))
        ########################FIG Block ends here############################

        ############Raghav Added This Block for MyAccount GG on 05/03/2022
        elif system == 'cbs_myaccount':
            try:
                date = object_key.split('/')[3].split('_')[-2] # This would be 'YYYY-mm-dd'
                table = object_key.split('/')[2]
                new_key = 'curated/cbs_myaccount/' + table + '/dt=' + date.lower() + '/' + object_key.split('/')[-1].replace('.parquet', '_uncompressed.parquet') #This would be File Name
                bucket.copy(copy_source, new_key)
                print("{} bucket_name = {} Object_Key={} Date={} Table={} New_Key={}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),bucket_name, object_key,date,table,new_key))
            except Exception as err:
                print("{} Message='File Process Failed, Please Check The Logs' Error={}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),err))
        ########################FIG Block ends here############################

        insert_file_log(aurora_credentials, datetime.now(), datetime.now(), 's3://' + bucket_name + '/' + object_key, 'SUCCESS', '')

    except Exception as err:
        print('File copy failed:', err)
        err_msg = str(err).replace("'", "").replace('"', '')
        insert_file_log(aurora_credentials, datetime.now(), datetime.now(), 's3://' + bucket_name + '/' + object_key, 'FAILED', err_msg[:2000])
