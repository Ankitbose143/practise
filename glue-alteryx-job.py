import sys

import time

import boto3

from awsglue.utils import getResolvedOptions

from pyspark.sql.functions import *

from pyspark.sql import SparkSession

from pyspark.context import SparkContext

from awsglue.context import GlueContext

from awsglue.job import Job

from pyspark.sql.types import DateType, TimestampType

from pyspark.sql import Window

import sys

import time

import boto3

 

 

 

# Get job parameters

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

 

# Initialize clients and contexts

athena_client = boto3.client("athena")

athena_client = boto3.client("athena")

sc = SparkContext()

glueContext = GlueContext(sc)

spark = glueContext.spark_session

job = Job(glueContext)

job.init(args["JOB_NAME"], args)

 

def athena_run(query):

    try:

        response = athena_client.start_query_execution(

            QueryString=query,

            QueryExecutionContext={"Database": "edw"}

        )

        print("Athena Data Read Completed")

        query_id = response["QueryExecutionId"]

        print(f"Query ID - {query_id}")

    except Exception as e:

        print(f"Error starting query execution: {e}")

        sys.exit(1)

 

    status = athena_client.get_query_execution(QueryExecutionId=query_id)["QueryExecution"]["Status"]["State"]

    while status.upper() in ["QUEUED", "RUNNING"]:

        print(f"Status of the query: {status}...")

        time.sleep(2)  # Wait for 2 seconds before checking again

        status = athena_client.get_query_execution(QueryExecutionId=query_id)["QueryExecution"]["Status"]["State"]

 

    res = athena_client.get_query_execution(QueryExecutionId=query_id)

    output_path = res["QueryExecution"]["ResultConfiguration"]["OutputLocation"]

    print(f"Query status - {status}")

    print(f"output path --> {output_path}")

 

    if status == "SUCCEEDED":

        print("Query executed successfully.")

        return output_path

    else:

        error_message = athena_client.get_query_execution(QueryExecutionId=query_id)["QueryExecution"]["Status"]["StateChangeReason"]

        print(f"Query failed or was cancelled. Reason: {error_message}")

        #sys.exit(1)

 

def add_prefix(df,prefix):

    for cols in df.columns:

        if cols != 'CUSTOMER_KEY':

            df = df.withColumnRenamed(cols,prefix+cols)

    return df

 

def read_athena_results(output_path):

    return spark.read.format("csv").option("header", "true").load(output_path)

 

query = """

    SELECT

        crf.TIME_KEY,

        crf.CUSTOMER_KEY,

        csd.SUB_STATUS_DESC,

        (CASE WHEN crf.PRICE_PROTECTION_FLAG = 'Y' THEN 1 ELSE 0 END) AS Service_Agreement,

        (CASE WHEN crf.EASY_PAY_FLAG = 'Y' THEN 1 ELSE 0 END) AS Easy_Pay,

        (CASE WHEN a12.ebill_flag = 1 THEN 1 ELSE 0 END) AS E_Bill

    FROM EDW.CUSTOMER_REVENUE_FACT crf

    JOIN edw.customer_substatus_dim csd ON csd.CUSTOMER_SUBSTATUS_KEY = crf.CUSTOMER_SUBSTATUS_KEY

    JOIN EDW.CHSI_TIER_MIGRATION_DIM CHSI ON CHSI.CHSI_TIER_MIGRATION_KEY = crf.CHSI_TIER_MIGRATION_KEY

    JOIN EDW.CUST_ACCT_SUM a12 ON crf.customer_key = a12.customer_key AND crf.TIME_KEY = a12.TIME_KEY

    WHERE date_parse(crf.TIME_KEY, '%Y-%m-%d') > date_trunc('month', date_add('month', -15, current_date - interval '1' day))

        AND crf.CUSTOMER_SUBSTATUS_KEY = 2

        AND CHSI.CHSI_TIER_MIGRATION_DESC NOT IN ('C2C CONNECT', 'STRAIGHTUP CONNECT')

"""

 

s3_path = athena_run(query)

df = read_athena_results(s3_path).dropDuplicates()

print("First DataFrame")

df.show()

 

q2 = """

    SELECT

        CAST(last_day_of_month(date_parse(WO_CHECKED_IN_DT_KEY, '%Y-%m-%d')) AS VARCHAR) AS TIME_KEY,

        CUSTOMER_KEY,

        CNCT_SALES_CHANNEL_KEY

    FROM EDW.SALES_WORK_ORDER_DLY_FACT

    WHERE CUSTOMER_SUBSTATUS_KEY = 2

        AND date_parse(WO_CHECKED_IN_DT_KEY, '%Y-%m-%d') > date_parse(date_format(date_trunc('month', last_day_of_month(date_add('month', -15, date_trunc('month', current_date - interval '1' day)))), '%Y-%m-%d'), '%Y-%m-%d')

"""

s3_path_2 = athena_run(q2)

df2 = read_athena_results(s3_path_2)

print("Second DataFrame Schema")

#df2.printSchema()

df2 = df2.select("TIME_KEY","CUSTOMER_KEY","CNCT_SALES_CHANNEL_KEY").distinct()

 

q3 = """SELECT sales_channel_key,sales_channel_hier_key FROM EDW.SALES_CHANNEL_DIM"""

q4 = """ SELECT SALES_CHANNEL_HIER_KEY,EMPLOYEE_TYPE_CD,SALES_SUB_CHANNEL_NM,SALES_CHANNEL_NM,AFFILIATE_NM,DISPLAY_CHANNEL_GROUP_NM FROM EDW.SALES_CHANNEL_HIER_DIM """

q5 = """SELECT

        crf.TIME_KEY,

        crf.CUSTOMER_KEY,

        csd.SUB_STATUS_DESC,

        (CASE WHEN crf.PRICE_PROTECTION_FLAG = 'Y' THEN 1 ELSE 0 END) AS Service_Agreement,

        (CASE WHEN crf.EASY_PAY_FLAG = 'Y' THEN 1 ELSE 0 END) AS Easy_Pay,

        (CASE WHEN a12.ebill_flag = 1 THEN 1 ELSE 0 END) AS E_Bill

        FROM

            EDW.CUSTOMER_REVENUE_FACT crf

        JOIN

            edw.customer_substatus_dim csd ON csd.CUSTOMER_SUBSTATUS_KEY = crf.CUSTOMER_SUBSTATUS_KEY

        JOIN

            EDW.CHSI_TIER_MIGRATION_DIM CHSI ON CHSI.CHSI_TIER_MIGRATION_KEY = crf.CHSI_TIER_MIGRATION_KEY

        JOIN

            EDW.CUST_ACCT_SUM a12 ON crf.customer_key = a12.customer_key AND crf.TIME_KEY = a12.TIME_KEY

        WHERE

            date_parse(crf.TIME_KEY, '%Y-%m-%d') > date_trunc('month', date_add('month', -15, current_date - interval '1' day))

            /*AND crf.CUSTOMER_SUBSTATUS_KEY IN (2,3)*/

            AND CHSI.CHSI_TIER_MIGRATION_DESC NOT IN ('C2C CONNECT', 'STRAIGHTUP CONNECT')

"""

s3_path_3 = athena_run(q3)

df3 = read_athena_results(s3_path_3).select("SALES_CHANNEL_KEY","SALES_CHANNEL_HIER_KEY")

 

s3_path_4 = athena_run(q4)

df4 = read_athena_results(s3_path_4).select("SALES_CHANNEL_HIER_KEY","EMPLOYEE_TYPE_CD","SALES_CHANNEL_NM","SALES_SUB_CHANNEL_NM","AFFILIATE_NM","DISPLAY_CHANNEL_GROUP_NM")

 

# Joining the DataFrames

joined_df = df.join(df2, ['TIME_KEY', 'CUSTOMER_KEY'], 'inner')

print("Joined data frame Schema")

joined_df.printSchema()

joined_df = joined_df.select("TIME_KEY","CUSTOMER_KEY","SUB_STATUS_DESC","SERVICE_AGREEMENT","EASY_PAY","E_BILL","CNCT_SALES_CHANNEL_KEY").distinct()

joined_df.printSchema()

joined_df = joined_df.join(df3, joined_df['CNCT_SALES_CHANNEL_KEY'] == df3['sales_channel_key'], 'inner').select(

    col('TIME_KEY'),

    col('CUSTOMER_KEY'),

    col('SUB_STATUS_DESC'),

    col('Service_Agreement'),

    col("CNCT_SALES_CHANNEL_KEY"),

    col('Easy_Pay'),

    col('E_Bill'),

    col('SALES_CHANNEL_HIER_KEY')

)

joined_df = joined_df.join(df4, 'SALES_CHANNEL_HIER_KEY', 'inner')

print("Joined df 4th schenma")

joined_df.printSchema()

# joined_df_2 = joined_df.join(df5,'CUSTOMER_KEY','inner')

# joined_df_2.show()

# Selecting and renaming the fields

renamed_df = joined_df.select(

    col('TIME_KEY'),

    col('CUSTOMER_KEY').cast("double"),

    col('SUB_STATUS_DESC'),

    col('Service_Agreement').cast("double"),

    col('Easy_Pay').cast("double"),

    col('E_Bill').cast("double"),

    col('EMPLOYEE_TYPE_CD').alias('ETC'),

    col('SALES_CHANNEL_NM').alias('CHANNEL'),

    col('SALES_SUB_CHANNEL_NM').alias('SUB_CHANNEL'),

    col('AFFILIATE_NM').alias('AFFILIATE'),

    col('DISPLAY_CHANNEL_GROUP_NM').alias('CHANNEL_GROUP')

)

 

 

transformed_df = renamed_df.groupBy(col("TIME_KEY").cast(TimestampType()).alias("Date"), "CHANNEL_GROUP", "CHANNEL", "SUB_CHANNEL", "Affiliate", "ETC").agg(sum("SERVICE_AGREEMENT").alias("Service Agreement"),sum("EASY_PAY").alias("Easy Pay"),sum("E_BILL").alias("eBill"),count("CUSTOMER_KEY").alias("Base Subs"))

print("str--> time")

transformed_df.select("Date").show(5)

transformed_df = transformed_df.withColumn(

    'CHANNEL_GROUP',

    when(col('CHANNEL_GROUP').isin(['Cox_Owned_Retail', 'Cox_Owned-Retail']), 'Retail')

    .when(col('CHANNEL_GROUP') == 'WebSales', 'Online')

    .otherwise(col('CHANNEL_GROUP'))

)

 

# Further transformations

transformed_df = transformed_df.withColumn(

    'Channel',

    when(col('Channel') == 'Web', 'Cox.com')

    .when(col('Channel') == 'eTail', 'eTailers')

    .when(col('Channel') == 'Third_Party_Online', 'National_Affiliates')

    .when(col('Sub_Channel').isNull(), col('CHANNEL_GROUP'))

    .when((col('Sub_Channel') == '3rd Party - Affinity') | (col('Sub_Channel') == 'Online - Referral'), 'National Affiliates')

    .when(col('Sub_Channel').contains('Online -'), 'Cox.com')

    .when(col('Sub_Channel') == '3rd Party - eTailer', 'eTailers')

    .when(col('Channel').isNull(), col('CHANNEL_GROUP'))

    .otherwise(col('Channel'))

)

 

path_to_s3 = "s3://cci-edo-data-workarea/alteryx_migration/athen_test_job/output_csv"

transformed_df.coalesce(1).write.csv(path_to_s3, header = True,mode='overwrite')

 

# ################# 2nd transformation or work flow #################################

 

s3_path_5 = athena_run(q5)

df5 = read_athena_results(s3_path_5)

df5 = add_prefix(df5,"R_")

df5.printSchema()

print("renamed_df-after casting")

renamed_df.printSchema()

transformed_df_2 = renamed_df.join(df5,"CUSTOMER_KEY","inner").select(col("R_SUB_STATUS_DESC").alias("Sub Status"),col("SUB_CHANNEL").alias("Sub Channel"),col("R_Service_Agreement").alias("Service Agreement"),"ETC",col("R_Easy_Pay").alias("Easy Pay"),col("R_E_Bill").alias("eBill"),col("R_TIME_KEY").alias("Date"),"CUSTOMER_KEY",col("TIME_KEY").alias("Connect Date"),col("CHANNEL_GROUP").alias("Channel Group"),col("CHANNEL").alias("Channel"),col("AFFILIATE").alias("Affiliate")).distinct()

transformed_df_2.printSchema()

 

transformed_df_2 = transformed_df_2.withColumn(

    'Channel Group',

    when(col('Channel Group').isin(['Cox_Owned_Retail', 'Cox_Owned-Retail']), 'Retail')

    .when(col('Channel Group') == 'Web Sales','Online')

    .otherwise(col('Channel Group'))

)

transformed_df_2 = transformed_df_2.withColumn(

    'Channel',

    when(col("Channel")=='Web','Cox.com')

    .when(col('Channel')=='Third Party Online','National Affiliates')

    .when((col('Sub Channel') == '3rd Party - Affinity') | (col('Sub Channel') == 'Online - Referral'), 'National Affiliates')

    .when(col('Sub Channel').contains('Online-'),'Cox.com')

    .when(col('Sub Channel') == '3rd Party - eTailer', 'eTailers')

    .when(col('Channel') == 'eTail', 'eTailers')

    .when(col('Channel').isNull(), col('Channel Group'))

    .otherwise(col('Channel'))

)

# #window over which lag would be applied

window = Window.orderBy("CUSTOMER_KEY","Channel Group","Date")

# print("Schema for the transformed_df_3")

# transformed_df_3.printSchema()

 

transformed_df_2 = transformed_df_2.withColumn(

    'Month Cohort',

    when(transformed_df_2['Sub Status'] == 'New', 0).otherwise(None)

)

 

transformed_df_2 = transformed_df_2.withColumn(

    'Month Cohort',

    when(col('Month Cohort')=='New',0)

    .otherwise(lag(col('Month Cohort'),1).over(window)+1)

)

transformed_df_2.printSchema()

 

# transformed_df_3.select('Month_Cohort').show()

 

grouped_transformed_df = transformed_df_2.groupBy("Month Cohort","Connect Date", "Channel Group","Channel","Sub Channel","Affiliate","ETC","Service Agreement","Easy Pay","eBill").agg(countDistinct("CUSTOMER_KEY").alias("Total Base"))

 

grouped_transformed_df.printSchema()

transformed_df_3 = grouped_transformed_df.select(

    col("Month Cohort"),

    col("Connect Date"),

    col("Channel Group"),

    col("Channel"),

    col("Sub Channel"),

    col("Affiliate"),

    col("ETC"),

    col("Service Agreement").cast("double"),

    col("Easy Pay").cast("double"),

    col("eBill"),

    col("Total Base").alias("Customers")

)

 

grouped_transformed_df_2 = grouped_transformed_df.groupBy("Month Cohort").agg(sum("Total Base").alias("Total Base"))

# grouped_transformed_df_2 = add_prefix(grouped_transformed_df_2,"R_")

grouped_transformed_df_2.printSchema()

transformed_df_3.printSchema()

 

final_transformed_df = transformed_df_3.join(grouped_transformed_df_2,"Month Cohort","inner")

print("Final transformed df Schema")

final_transformed_df.printSchema()

final_transformed_df = final_transformed_df.withColumn(

    "Mix",

    when((col("Service Agreement") == 0) & (col("Easy Pay") == 0), "None")

    .when((col("Service Agreement") == 1) & (col("Easy Pay") == 0), "SA Only")

    .when((col("Service Agreement") == 0) & (col("Easy Pay") == 1), "EP Only")

    .when((col("Service Agreement") == 1) & (col("Easy Pay") == 1), "Both")

    .otherwise(None)

)

final_transformed_df = final_transformed_df.groupBy(

    "Month Cohort",

    "Connect Date",

    "Channel Group",

    "Channel",

    "Sub Channel",

    "Affiliate",

    "ETC",

    "Mix"

).agg(

    sum("Customers").alias("Customers"),   # Aggregating the count of customers

    sum("Total Base").alias("Total Base")    # Summing the Total Base

)

final_transformed_df.printSchema()

final_transformed_df.show(5)

path_to_s3 = "s3://cci-edo-data-workarea/alteryx_migration/athen_test_job_part_2/output_csv"

transformed_df.coalesce(1).write.csv(path_to_s3,header = True, mode='overwrite')

# Commit the Glue job

job.commit()