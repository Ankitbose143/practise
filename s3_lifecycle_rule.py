import boto3
import pymysql
import json
import logging
import os
from datetime import datetime

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 and RDS clients
s3_client = boto3.client('s3')
rds_client = pymysql


def get_secret():
    try:
        secret_name = os.environ['env_var_mysqldb_credentials']
        region_name = "us-east-1"
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        
        return json.loads(secret)
        
    except Exception as err:
        logger.error("Get secret error: {0}".format(err))
        raise

def make_connection():
    secret = get_secret()
    endpoint = secret['host']
    port = secret['port']
    dbuser = secret['username']
    password = secret['password']
    database = secret['dbname']
    
    return pymysql.connect(host=endpoint, user=dbuser, passwd=password,
                          port=int(port), db=database, autocommit=True)

def get_s3_lifecycle_config():
    all_lifecycle_policies = []
    try:
        # Get all S3 buckets
        buckets = s3_client.list_buckets().get('Buckets', [])
        
        for bucket in buckets:
            bucket_name = bucket['Name']
            try:
                # Get lifecycle configuration for each bucket
                lifecycle_response = s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
                rules = lifecycle_response.get('Rules', [])
                
                for rule in rules:
                    # Check if Expiration rule exists
                    status = rule.get('Status', 'No status specified')
                    expiration = rule.get('Expiration', {})
                    retention_period = expiration.get('Days', 'No expiration specified')

                    # If retention period is 0, treat it as valid
                    if retention_period == 0:
                        retention_period = '0 days (lifecycle configured)'
                    
                    # Handle NoncurrentVersionExpiration rule
                    noncurrent_version_expiration = rule.get('NoncurrentVersionExpiration', {})
                    noncurrent_retention_period = noncurrent_version_expiration.get('NoncurrentDays', 'No noncurrent expiration specified')

                    # Handle Incomplete Multipart Upload (AbortIncompleteMultipartUpload)
                    abort_multipart = rule.get('AbortIncompleteMultipartUpload', {})
                    abort_multipart_days = abort_multipart.get('DaysAfterInitiation', None)

                    # Skip null values for abort multipart uploads
                    abort_multipart_days = abort_multipart_days if abort_multipart_days is not None else 'No multipart upload specified'

                    # Get rule prefix and ID (if present)
                    lifecycle_name = rule.get('ID', 'No ID')
                    filter_condition = rule.get('Filter', {})
                    lifecycle_prefix = filter_condition.get('Prefix', '') if 'Prefix' in filter_condition else ''

                    # Build bucket path and append lifecycle details
                    bucket_path = f"s3://{bucket_name}/{lifecycle_prefix}"
                    all_lifecycle_policies.append({
                        'BucketName': bucket_name,
                        'BucketPath': bucket_path,
                        'RetentionPeriod': retention_period,
                        'LifecycleName': lifecycle_name,
                        'Prefix': lifecycle_prefix,
                        'NoncurrentRetentionPeriod': noncurrent_retention_period,
                        'AbortMultipartDays': abort_multipart_days,
                        'Status': status
                    })
            except s3_client.exceptions.ClientError as e:
                logger.error(f"Error getting lifecycle configuration for bucket {bucket_name}: {e}")
    except Exception as err:
        logger.error(f"Error listing S3 buckets: {err}")
        raise

    return all_lifecycle_policies


def lambda_handler(event, context):
    environment = os.environ.get('ENVIRONMENT', 'dev')  # Default to 'dev' if not set
    schema_name = 'dev_data_profiler' if environment == 'dev' else 'data_profiler'
    # Connect to RDS
    try:
        cnx = make_connection()
        cursor = cnx.cursor()
    except Exception as err:
        logger.error("Error connecting to RDS: {0}".format(err))
        raise

    # Get S3 lifecycle configurations
    s3_lifecycle_configs = get_s3_lifecycle_config()
    
    # Insert or update records with S3 bucket path and retention period
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for details in s3_lifecycle_configs:
        bucket_path = details['BucketPath']
        bucket_name = details['BucketName']
        retention_period = details['RetentionPeriod']
        lifecycle_name = details['LifecycleName']
        prefix = details['Prefix'] if details['Prefix'] else ''  # Ensure prefix is not None
        noncurrent_retention_period = details['NoncurrentRetentionPeriod']
        abort_multipart_days = details['AbortMultipartDays'] 
        status = details['Status']

        # Log the details being processed
        logger.info(f"Processing bucket: {bucket_name}, path: {bucket_path}, prefix: {prefix}")

        # Check if record exists
        check_query = f"""SELECT COUNT(*) FROM dev_data_profiler.S3_Lifecycle_Config WHERE S3_BUCKET = '{bucket_name}' AND PREFIX = '{prefix}' AND CURRENT_VERSION_RETENTION = '{retention_period}' AND NON_CURRENT_VERSION_RETENTION = '{noncurrent_retention_period}' AND STATUS = '{status}' AND INCOMPLETE_MULTIPART_UPLOAD = '{abort_multipart_days}'"""
        
        cursor.execute(check_query)
        result = cursor.fetchone()
        logger.info(f"Check query result for bucket {bucket_name} with prefix {prefix}: {result}")

        if result[0] == 0:
            # Record does not exist, perform insert
            insert_query = f"""
            INSERT INTO {schema_name}.S3_Lifecycle_Config (
                LIFECYCLE_NAME,          -- lifecycle name
                LAST_UPDATE_DT,         -- LAST_UPDATE_DT
                S3_BUCKET,              -- S3_BUCKET
                PREFIX,                 -- prefix
                CURRENT_VERSION_RETENTION,       -- RETENTION_PERIOD
                NON_CURRENT_VERSION_RETENTION, -- Noncurrent retention period
                STATUS,               -- Status (Enabled/Disabled)
                INCOMPLETE_MULTIPART_UPLOAD
            ) VALUES (
                '{lifecycle_name}',       -- lifecycle name
                TIMESTAMP('{update_time}'),  -- LAST_UPDATE_DT
                '{bucket_name}',          -- S3_BUCKET
                '{prefix}',               -- PREFIX
                '{retention_period}',       -- RETENTION_PERIOD
                '{noncurrent_retention_period}', -- NON_CURRENT_PERIOD
                '{status}',             -- Status (Enabled/Disabled)
                '{abort_multipart_days}'  -- Incomplete multipart upload days
            )
            """
            logger.info(f"Executing insert query: {insert_query}")
            try:
                cursor.execute(insert_query)
                cnx.commit()  # Ensure the transaction is committed
                logger.info(f"Successfully inserted lifecycle rule {lifecycle_name} for bucket: {details['BucketName']}")
            except Exception as err:
                logger.error(f"Cannot execute insert query for bucket {details['BucketName']}: {err}")

        else:
            # Record exists, perform update
            update_query = f"""
            UPDATE {schema_name}.S3_Lifecycle_Config
            SET
                LAST_UPDATE_DT = TIMESTAMP('{update_time}'),
                CURRENT_VERSION_RETENTION = '{retention_period}',
                PREFIX = '{prefix}',
                LIFECYCLE_NAME = '{lifecycle_name}',
                NON_CURRENT_VERSION_RETENTION = '{noncurrent_retention_period}',
                INCOMPLETE_MULTIPART_UPLOAD = '{abort_multipart_days}',
                STATUS = '{status}'
            WHERE S3_BUCKET = '{bucket_name}' AND PREFIX = '{prefix}' AND CURRENT_VERSION_RETENTION = '{retention_period}' AND NON_CURRENT_VERSION_RETENTION = '{noncurrent_retention_period}' AND STATUS = '{status}' AND INCOMPLETE_MULTIPART_UPLOAD = '{abort_multipart_days}'
            """
            logger.info(f"Executing update query: {update_query}")
            try:
                cursor.execute(update_query)
                cnx.commit()
                logger.info(f"Successfully updated lifecycle rule {lifecycle_name} for bucket: {details['BucketName']}")
            except Exception as err:
                logger.error(f"Cannot execute update query for bucket {details['BucketName']}: {err}")

    cursor.close()
    cnx.close()
    return {
        'statusCode': 200,
        'body': json.dumps('S3 lifecycle configurations processed successfully.')
    }
