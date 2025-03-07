# ****************************** DEV NOTE ************************************************************************
# AUTHOR:              [Ankit Bose]
# VERSION:             1.0
# BUILD DATE:          [2024-10-07]
# FRAMEWORK NAME:      [digital_mkt_ds_revenue_stg]
# FUNCTIONALITY:     
#     This AWS Glue job [digital_mkt_ds_revenue_stg] is designed to:
# - [Functionality :This process involves extracting data from an S3 bucket, processing the data using specific SQL queries from the respective module, and then loading the results into another S3 bucket. This loaded data then triggers a second Glue job named digital_mkt_ds_revenue_final. This second Glue job performs further processing and ultimately facilitates an incremental load.
# - The process is divided into separate Glue jobs to enhance processing speed and optimize handling of large datasets over time.]
# INVOCATIONS:
#     - TRIGGERED BY:       Scheduled CloudWatch Event
#     - SCHEDULE:           [Recurring, at 12:00 PM EST(5:00 pm UTC)]
# # DEPLOYMENT DETAILS:
#     -S3 Buckets Used:    - Input: s3://[s3://cci-edo-data-workarea/alteryx_digital_marketing/ds_revenue/input/]
#                           - Output:s3://cci-edo-data-workarea/alteryx_digital_marketing/ds_revenue/output/cro_eligibility_limits_prepost_final_union/,
#                                   s3://[s3://cci-edo-data-workarea/alteryx_digital_marketing/ds_revenue/output/]
# ****************************** DEV NOTE ************************************************************************

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import lit, expr
from pyspark.storagelevel import StorageLevel 
import boto3 # type: ignore
# from utils.ReadUtil import createTempView
# from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import spark_partition_id

from awsglue.utils import getResolvedOptions #type: ignore
from pyspark.sql.functions import col, when, sum, count, lag
global spark
from pyspark.sql.types import StructType, StructField, StringType , IntegerType
from pyspark.sql.functions import to_date

from pyspark.sql import functions as F
from awsglue.dynamicframe import DynamicFrame
import sys
import io
import gc
import logging
import datetime
from utils.loggerUtils import print_debug, PrintException
from utils.sparkUtils import get_spark_session, get_source_dataframes
from utils.dataLoadUtils import writeTable
from adobe_config_read import QueryAthena

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from DSREVENUE import DSREVENUE
from DSREVENUE2 import DSREVENUE2
from DSREVENUE3 import DSREVENUE3
from DSREVENUE4 import DSREVENUE4
from DSREVENUE5 import DSREVENUE5
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
    
glue_client = boto3.client('glue')
global database_nm
log_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def create_and_initialize_global_spark_session():
    global spark, job, glueContext, log_time

    # spark = create_spark_session("digital_marketing")
    # configure_s3_permissions()
    log_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    sc = SparkContext()
    args = getResolvedOptions(sys.argv, ['JOB_NAME'])
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args['JOB_NAME'], args)
    spark._jsc.hadoopConfiguration().set("fs.s3.useRequesterPaysHeader", "true")
    spark._jsc.hadoopConfiguration().set("fs.s3a.fast.upload", "true")
    athena_client = boto3.client('athena')
    spark.conf.set("spark.sql.shuffle.partitions", "3000")  # Adjust based on your data size and available executors
    
    
    # Enable Adaptive Query Execution (AQE)
    spark.conf.set("spark.sql.adaptive.enabled", "true")
    
    
def create_and_initialize_log(database_nm):
    try:
        insert_log_pquery = f"""
                                    INSERT INTO {database_nm}.digital_mkt_process_auditlog  
                                    (process_id, job_id, job_nm, process_nm, process_status, process_start_dt, process_end_dt,retry_count) 
                                    VALUES ('5700', 5700, 'digital_mkt_ds_revenue_stg', 'digital_mkt_ds_revenue_stg', 'InProgress',TIMESTAMP '{log_time}', NULL,0)
                                """
                        
        insert_log_progress = QueryAthena(query=insert_log_pquery, database=database_nm)
        insert_log_progress.run_query(False)
    except Exception as err:
        logger.error(f"Error in inserting audit log : {str(err)}")
        raise
    
def get_bucket_file_path(historical_data_s3_path):
    try:
        splited_path = historical_data_s3_path.removeprefix("s3://").split("/")
        (bucket, prefix) = (splited_path[0], "/".join(splited_path[1:]))
        return (bucket, prefix)
    except Exception as err:
        print("Error", str(err))



def main():
    """
    Main function to initialize spark session
    """
    create_and_initialize_global_spark_session()
    try:
        args = getResolvedOptions(sys.argv, ['output_path','historical_data_s3_path', 'target_file_path','target_file_path2','target_file_path3', 'partition_column', 'partition_format', 'database_nm', 'table_nm', 'table_nm2','table_nm3', 'bucket', 'target_job_name'])
        
        # Access the bucket parameter
        
        output_path = args['output_path']
        historical_data_s3_path = args['historical_data_s3_path']
        partition_column = args['partition_column']
        partition_format = args['partition_format']
        database_nm = args['database_nm']
        table_nm = args['table_nm']
        table_nm2 = args['table_nm2']
        table_nm3 = args['table_nm3']
        target_file_path = args['target_file_path']
        target_file_path2 = args['target_file_path2']
        target_file_path3 = args['target_file_path3']
        target_job_name = args['target_job_name']
        # bucket = args['bucket']
        
        create_and_initialize_log(database_nm)
        
        # This func join revenue query with CS_EMPLOYEE_TYPE_CD_XREF table on ETC column, follwed by joining on customer_substatus_dim
        # on customer_substatus_key columns with group by on all the columns
        net_revenue_and_sales_channel_join_query = spark.sql(DSREVENUE.net_revenue_and_sales_channel_join_query())
        
        logger.info(f"Function: net_revenue_and_sales_channel_join_query | Row show: {net_revenue_and_sales_channel_join_query.show(5)}")
        logger.info(f"Function: net_revenue_and_sales_channel_join_query | Row Count: {net_revenue_and_sales_channel_join_query.count()}")
        net_revenue_and_sales_channel_join_query.createOrReplaceTempView("net_revenue_and_sales_channel_join_query")
        net_revenue_and_sales_channel_join_query.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'net_revenue_and_sales_channel_join_query/')

        
        
        net_revenue_and_sales_channel_join_query_psu = spark.sql(DSREVENUE.net_revenue_and_sales_channel_join_query_psu())
        net_revenue_and_sales_channel_join_query_psu.createOrReplaceTempView("net_revenue_and_sales_channel_join_query_psu")
        logger.info(f"Function: net_revenue_and_sales_channel_join_query_psu | Row show: {net_revenue_and_sales_channel_join_query_psu.show(5)}")
        logger.info(f"Function: net_revenue_and_sales_channel_join_query_psu | Row Count: {net_revenue_and_sales_channel_join_query_psu.count()}")
        net_revenue_and_sales_channel_join_query_psu.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'net_revenue_and_sales_channel_join_query_psu/')
        
        net_revenue_and_sales_channel_join_query2 = spark.sql(DSREVENUE.net_revenue_and_sales_channel_join_query2("net_revenue_and_sales_channel_join_query"))
        net_revenue_and_sales_channel_join_query2.createOrReplaceTempView("net_revenue_and_sales_channel_join_query2")
        # logger.info(f"Function: net_revenue_and_sales_channel_join_query2 | Row show: {net_revenue_and_sales_channel_join_query2.show(5)}")
        # logger.info(f"Function: net_revenue_and_sales_channel_join_query2 | Row Count: {net_revenue_and_sales_channel_join_query2.count()}")
        net_revenue_and_sales_channel_join_query2.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'net_revenue_and_sales_channel_join_query2/')
        
        net_revenue_and_sales_channel_join_query2_psu = spark.sql(DSREVENUE.net_revenue_and_sales_channel_join_query2("net_revenue_and_sales_channel_join_query_psu"))
        net_revenue_and_sales_channel_join_query2_psu.createOrReplaceTempView("net_revenue_and_sales_channel_join_query2_psu")
        # logger.info(f"Function: net_revenue_and_sales_channel_join_query2_psu | Row show: {net_revenue_and_sales_channel_join_query2_psu.show(5)}")
        # logger.info(f"Function: net_revenue_and_sales_channel_join_query2_psu | Row Count: {net_revenue_and_sales_channel_join_query2_psu.count()}")
        net_revenue_and_sales_channel_join_query_psu.unpersist()
        spark.catalog.dropTempView("net_revenue_and_sales_channel_join_query_psu")
        net_revenue_and_sales_channel_join_query2_psu.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'net_revenue_and_sales_channel_join_query2_psu/')
        
        net_revenue_and_sales_channel_join_query3 = spark.sql(DSREVENUE.net_revenue_and_sales_channel_join_query3("net_revenue_and_sales_channel_join_query2"))
        net_revenue_and_sales_channel_join_query3.createOrReplaceTempView("net_revenue_and_sales_channel_join_query3")
        # logger.info(f"Function: net_revenue_and_sales_channel_join_query3 | Row show: {net_revenue_and_sales_channel_join_query3.show(5)}")
        # logger.info(f"Function: net_revenue_and_sales_channel_join_query3 | Row Count: {net_revenue_and_sales_channel_join_query3.count()}")
        net_revenue_and_sales_channel_join_query.unpersist()
        spark.catalog.dropTempView("net_revenue_and_sales_channel_join_query")
        
        net_revenue_and_sales_channel_join_query3_psu = spark.sql(DSREVENUE.net_revenue_and_sales_channel_join_query3("net_revenue_and_sales_channel_join_query2_psu"))
        net_revenue_and_sales_channel_join_query3_psu.createOrReplaceTempView("net_revenue_and_sales_channel_join_query3_psu")
        # logger.info(f"Function: net_revenue_and_sales_channel_join_query3_psu | Row show: {net_revenue_and_sales_channel_join_query3_psu.show(5)}")
        # logger.info(f"Function: net_revenue_and_sales_channel_join_query3_psu | Row Count: {net_revenue_and_sales_channel_join_query3_psu.count()}")
        net_revenue_and_sales_channel_join_query2_psu.unpersist()
        spark.catalog.dropTempView("net_revenue_and_sales_channel_join_query2_psu")
        
        net_revenue_and_sales_channel_join_query4 = spark.sql(DSREVENUE.net_revenue_and_sales_channel_join_query4("net_revenue_and_sales_channel_join_query3"))
        net_revenue_and_sales_channel_join_query4.createOrReplaceTempView("net_revenue_and_sales_channel_join_query4")
        # logger.info(f"Function: net_revenue_and_sales_channel_join_query4 | Row show: {net_revenue_and_sales_channel_join_query4.show(5)}")
        # logger.info(f"Function: net_revenue_and_sales_channel_join_query4 | Row Count: {net_revenue_and_sales_channel_join_query4.count()}")
        spark.catalog.dropTempView("net_revenue_and_sales_channel_join_query2")
        
        net_revenue_and_sales_channel_join_query5 = spark.sql(DSREVENUE.net_revenue_and_sales_channel_join_query5("net_revenue_and_sales_channel_join_query3_psu"))
        net_revenue_and_sales_channel_join_query5.createOrReplaceTempView("net_revenue_and_sales_channel_join_query5")
        # logger.info(f"Function: net_revenue_and_sales_channel_join_query5 | Row show: {net_revenue_and_sales_channel_join_query5.show(5)}")
        # logger.info(f"Function: net_revenue_and_sales_channel_join_query5 | Row Count: {net_revenue_and_sales_channel_join_query5.count()}")
        net_revenue_and_sales_channel_join_query3_psu.unpersist()
        spark.catalog.dropTempView("net_revenue_and_sales_channel_join_query3_psu")
        
        net_revenue_and_sales_channel_join_final = spark.sql(DSREVENUE.net_revenue_and_sales_channel_join_final("net_revenue_and_sales_channel_join_query4", "net_revenue_and_sales_channel_join_query5"))
        net_revenue_and_sales_channel_join_final.createOrReplaceTempView("net_revenue_and_sales_channel_join_final")
        logger.info(f"Function: net_revenue_and_sales_channel_join_final | Executed")
        # logger.info(f"Function: net_revenue_and_sales_channel_join_final | Row show: {net_revenue_and_sales_channel_join_final.show(5)}")
        # logger.info(f"Function: net_revenue_and_sales_channel_join_final | Row Count: {net_revenue_and_sales_channel_join_final.count()}")
        spark.catalog.dropTempView("net_revenue_and_sales_channel_join_query5")
        net_revenue_and_sales_channel_join_final.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'net_revenue_and_sales_channel_join_final/')

        nrpa_account_changed = spark.sql(DSREVENUE.nrpa_account_changed("net_revenue_and_sales_channel_join_query3"))
        nrpa_account_changed.createOrReplaceTempView("nrpa_account_changed")
        # logger.info(f"Function: nrpa_account_changed | Row show: {nrpa_account_changed.show(5)}")
        # logger.info(f"Function: nrpa_account_changed | Row Count: {nrpa_account_changed.count()}")
        spark.catalog.dropTempView("net_revenue_and_sales_channel_join_query4")

        nrpa_account_changed1 = spark.sql(DSREVENUE.nrpa_account_changed1("nrpa_account_changed"))
        nrpa_account_changed1.createOrReplaceTempView("nrpa_account_changed1")
        # logger.info(f"Function: nrpa_account_changed1 | Row show: {nrpa_account_changed1.show(5)}")
        # logger.info(f"Function: nrpa_account_changed1 | Row Count: {nrpa_account_changed1.count()}")
        spark.catalog.dropTempView("nrpa_account_changed")
        
        account_changed_all = spark.sql(DSREVENUE.account_changed_all("net_revenue_and_sales_channel_join_query3"))
        account_changed_all.createOrReplaceTempView("account_changed_all")
        # logger.info(f"Function: account_changed_all | Row show: {account_changed_all.show(5)}")
        # logger.info(f"Function: account_changed_all | Row Count: {account_changed_all.count()}")
        net_revenue_and_sales_channel_join_query3.unpersist()
        spark.catalog.dropTempView("net_revenue_and_sales_channel_join_query3")
        
        nrpa_account_changed_union = spark.sql(DSREVENUE.nrpa_account_changed_union("nrpa_account_changed1", "account_changed_all"))
        nrpa_account_changed_union.createOrReplaceTempView("nrpa_account_changed_union")
        # logger.info(f"Function: nrpa_account_changed_union | Row show: {nrpa_account_changed_union.show(5)}")
        # logger.info(f"Function: nrpa_account_changed_union | Row Count: {nrpa_account_changed_union.count()}")
        nrpa_account_changed_union.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'nrpa_account_changed_union/')
        
        nrpa_account_changed_union_sum = spark.sql(DSREVENUE.nrpa_account_changed_union_sum("nrpa_account_changed_union"))
        nrpa_account_changed_union_sum.createOrReplaceTempView("nrpa_account_changed_union_sum")
        # logger.info(f"Function: nrpa_account_changed_union_sum | Row show: {nrpa_account_changed_union_sum.show(5)}")
        # logger.info(f"Function: nrpa_account_changed_union_sum | Row Count: {nrpa_account_changed_union_sum.count()}")
        spark.catalog.dropTempView("account_changed_all")
        spark.catalog.dropTempView("nrpa_account_changed1")
        nrpa_account_changed_union_sum.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'nrpa_account_changed_union_sum/')
        
        net_revenue_and_account_changed_union = spark.sql(DSREVENUE.net_revenue_and_account_changed_union("net_revenue_and_sales_channel_join_final", "nrpa_account_changed_union_sum"))
        net_revenue_and_account_changed_union.createOrReplaceTempView("net_revenue_and_account_changed_union")
        # logger.info(f"Function: net_revenue_and_account_changed_union | Row show: {net_revenue_and_account_changed_union.show(5)}")
        # logger.info(f"Function: net_revenue_and_account_changed_union | Row Count: {net_revenue_and_account_changed_union.count()}")
        net_revenue_and_sales_channel_join_final.unpersist()
        spark.catalog.dropTempView("net_revenue_and_sales_channel_join_final")
        net_revenue_and_account_changed_union.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'net_revenue_and_account_changed_union/')
        

        net_revenue_and_account_changed_union_sum = spark.sql(DSREVENUE.net_revenue_and_account_changed_union_sum("net_revenue_and_account_changed_union"))
        net_revenue_and_account_changed_union_sum.createOrReplaceTempView("net_revenue_and_account_changed_union_sum")
        # logger.info(f"Function: net_revenue_and_account_changed_union_sum | Row show: {net_revenue_and_account_changed_union_sum.show(5)}")
        # logger.info(f"Function: net_revenue_and_account_changed_union_sum | Row Count: {net_revenue_and_account_changed_union_sum.count()}")
        nrpa_account_changed_union_sum.unpersist()
        spark.catalog.dropTempView("nrpa_account_changed_union_sum")
        net_revenue_and_account_changed_union_sum.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'net_revenue_and_account_changed_union_sum/')
        
        net_revenue_and_account_changed_union_sum_dscg = spark.sql(DSREVENUE.net_revenue_and_account_changed_union_sum_dscg("net_revenue_and_account_changed_union_sum"))
        net_revenue_and_account_changed_union_sum_dscg.createOrReplaceTempView("net_revenue_and_account_changed_union_sum_dscg")
        # logger.info(f"Function: net_revenue_and_account_changed_union_sum_dscg | Row show: {net_revenue_and_account_changed_union_sum_dscg.show(5)}")
        # logger.info(f"Function: net_revenue_and_account_changed_union_sum_dscg | Row Count: {net_revenue_and_account_changed_union_sum_dscg.count()}")
        spark.catalog.dropTempView("net_revenue_and_account_changed_union")
        net_revenue_and_account_changed_union_sum_dscg.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'net_revenue_and_account_changed_union_sum_dscg/')
        
        net_revenue_and_account_changed_union_sum_dscg_not = spark.sql(DSREVENUE.net_revenue_and_account_changed_union_sum_dscg_not("net_revenue_and_account_changed_union_sum"))
        net_revenue_and_account_changed_union_sum_dscg_not.createOrReplaceTempView("net_revenue_and_account_changed_union_sum_dscg_not")
        # logger.info(f"Function: net_revenue_and_account_changed_union_sum_dscg_not | Row show: {net_revenue_and_account_changed_union_sum_dscg_not.show(5)}")
        # logger.info(f"Function: net_revenue_and_account_changed_union_sum_dscg_not | Row Count: {net_revenue_and_account_changed_union_sum_dscg_not.count()}")
        net_revenue_and_account_changed_union.unpersist()
        net_revenue_and_account_changed_union_sum.unpersist()
        spark.catalog.dropTempView("nrpa_account_changed_union")
        spark.catalog.dropTempView("net_revenue_and_account_changed_union_sum")
        net_revenue_and_account_changed_union_sum_dscg_not.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'net_revenue_and_account_changed_union_sum_dscg_not/')
        
        current_sch = spark.sql(DSREVENUE.current_sch())
        current_sch.createOrReplaceTempView("current_sch")
        # logger.info(f"Function: current_sch | Row show: {current_sch.show(5)}")
        # logger.info(f"Function: current_sch | Row Count: {current_sch.count()}")
        
        current_sch_join = spark.sql(DSREVENUE.current_sch_join("net_revenue_and_account_changed_union_sum_dscg","current_sch"))
        current_sch_join.createOrReplaceTempView("current_sch_join")
        # logger.info(f"Function: current_sch_join | Row show: {current_sch_join.show(5)}")
        # logger.info(f"Function: current_sch_join | Row Count: {current_sch_join.count()}")
        spark.catalog.dropTempView("net_revenue_and_account_changed_union_sum_dscg")
        
        current_sch_join_union = spark.sql(DSREVENUE.current_sch_join_union("net_revenue_and_account_changed_union_sum_dscg_not","current_sch_join"))
        current_sch_join_union.createOrReplaceTempView("current_sch_join_union")
        # logger.info(f"Function: current_sch_join_union | Row show: {current_sch_join_union.show(5)}")
        # logger.info(f"Function: current_sch_join_union | Row Count: {current_sch_join_union.count()}")
        net_revenue_and_account_changed_union_sum.unpersist()
        spark.catalog.dropTempView("net_revenue_and_account_changed_union_sum")
        spark.catalog.dropTempView("current_sch")
        current_sch_join_union.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'current_sch_join_union/')
        
        current_sch_join_union_rename = spark.sql(DSREVENUE.current_sch_join_union_rename("current_sch_join_union"))
        current_sch_join_union_rename.createOrReplaceTempView("current_sch_join_union_rename")
        # logger.info(f"Function: current_sch_join_union_rename | Row show: {current_sch_join_union_rename.show(5)}")
        # logger.info(f"Function: current_sch_join_union_rename | Row Count: {current_sch_join_union_rename.count()}")
        net_revenue_and_account_changed_union_sum_dscg_not.unpersist()
        spark.catalog.dropTempView("net_revenue_and_account_changed_union_sum_dscg_not")
        spark.catalog.dropTempView("current_sch_join")
        net_revenue_and_account_changed_union_sum_dscg_not.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'net_revenue_and_account_changed_union_sum_dscg_not/')
        
        rdt_nrp_swodf = spark.sql(DSREVENUE.rdt_nrp_swodf())
        rdt_nrp_swodf.createOrReplaceTempView("rdt_nrp_swodf")
        # logger.info(f"Function: rdt_nrp_swodf | Row show: {rdt_nrp_swodf.show(5)}")
        # logger.info(f"Function: rdt_nrp_swodf | Row Count: {rdt_nrp_swodf.count()}")
        current_sch_join_union.unpersist()
        spark.catalog.dropTempView("current_sch_join_union")
        rdt_nrp_swodf.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf/')
        
        rdt_nrp_swodf_mirations = spark.sql(DSREVENUE.rdt_nrp_swodf_mirations())
        rdt_nrp_swodf_mirations.createOrReplaceTempView("rdt_nrp_swodf_mirations")
        # logger.info(f"Function: rdt_nrp_swodf_mirations | Row show: {rdt_nrp_swodf_mirations.show(5)}")
        # logger.info(f"Function: rdt_nrp_swodf_mirations | Row Count: {rdt_nrp_swodf_mirations.count()}")
        rdt_nrp_swodf_mirations.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_mirations/')
        
        rdt_nrp_swodf_offers = spark.sql(DSREVENUE.rdt_nrp_swodf_offers())
        rdt_nrp_swodf_offers.createOrReplaceTempView("rdt_nrp_swodf_offers")
        # logger.info(f"Function: rdt_nrp_swodf_offers | Row show: {rdt_nrp_swodf_offers.show(5)}")
        # logger.info(f"Function: rdt_nrp_swodf_offers | Row Count: {rdt_nrp_swodf_offers.count()}")
        rdt_nrp_swodf_offers.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_offers/')
        
        rdt_nrp_swodf_campaign_codes = spark.sql(DSREVENUE.rdt_nrp_swodf_campaign_codes())
        rdt_nrp_swodf_campaign_codes.createOrReplaceTempView("rdt_nrp_swodf_campaign_codes")
        # logger.info(f"Function: rdt_nrp_swodf_campaign_codes | Row show: {rdt_nrp_swodf_campaign_codes.show(5)}")
        # logger.info(f"Function: rdt_nrp_swodf_campaign_codes | Row Count: {rdt_nrp_swodf_campaign_codes.count()}")
        rdt_nrp_swodf_campaign_codes.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_campaign_codes/')
        
        rdt_nrp_swodf_first_join = spark.sql(DSREVENUE.rdt_nrp_swodf_first_join("current_sch_join_union_rename", "rdt_nrp_swodf"))
        rdt_nrp_swodf_first_join.createOrReplaceTempView("rdt_nrp_swodf_first_join")
        # logger.info(f"Function: rdt_nrp_swodf_first_join | Row show: {rdt_nrp_swodf_first_join.show(5)}")
        # logger.info(f"Function: rdt_nrp_swodf_first_join | Row Count: {rdt_nrp_swodf_first_join.count()}")
        spark.catalog.dropTempView("current_sch_join_union_rename")
        rdt_nrp_swodf_first_join.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_first_join/')
        
        rdt_nrp_swodf_second_join = spark.sql(DSREVENUE.rdt_nrp_swodf_second_join("rdt_nrp_swodf_first_join", "rdt_nrp_swodf_mirations"))
        rdt_nrp_swodf_second_join.createOrReplaceTempView("rdt_nrp_swodf_second_join")
        # logger.info(f"Function: rdt_nrp_swodf_second_join | Row show: {rdt_nrp_swodf_second_join.show(5)}")
        # logger.info(f"Function: rdt_nrp_swodf_second_join | Row Count: {rdt_nrp_swodf_second_join.count()}")
        rdt_nrp_swodf_first_join.unpersist()
        spark.catalog.dropTempView("rdt_nrp_swodf_first_join")
        spark.catalog.dropTempView("rdt_nrp_swodf")
        rdt_nrp_swodf_second_join.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_second_join/')
        
        rdt_nrp_swodf_third_join = spark.sql(DSREVENUE.rdt_nrp_swodf_third_join("rdt_nrp_swodf_second_join", "rdt_nrp_swodf_offers"))
        rdt_nrp_swodf_third_join.createOrReplaceTempView("rdt_nrp_swodf_third_join")
        # logger.info(f"Function: rdt_nrp_swodf_third_join | Row show: {rdt_nrp_swodf_third_join.show(5)}")
        # logger.info(f"Function: rdt_nrp_swodf_third_join | Row Count: {rdt_nrp_swodf_third_join.count()}")
        rdt_nrp_swodf_second_join.unpersist()
        spark.catalog.dropTempView("rdt_nrp_swodf_second_join")
        rdt_nrp_swodf_third_join.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_third_join/')
        
        rdt_nrp_swodf_fourth_join = spark.sql(DSREVENUE.rdt_nrp_swodf_fourth_join("rdt_nrp_swodf_third_join", "rdt_nrp_swodf_campaign_codes"))
        rdt_nrp_swodf_fourth_join.createOrReplaceTempView("rdt_nrp_swodf_fourth_join")
        logger.info(f"Function: rdt_nrp_swodf_fourth_join | Executed")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join | Row show: {rdt_nrp_swodf_fourth_join.show(5)}")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join | Row Count: {rdt_nrp_swodf_fourth_join.count()}")
        rdt_nrp_swodf_third_join.unpersist()
        spark.catalog.dropTempView("rdt_nrp_swodf_third_join")
        rdt_nrp_swodf_fourth_join.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_fourth_join/')
        
        # rdt_nrp_swodf_fourth_join_case
        rdt_nrp_swodf_fourth_join_case = spark.sql(DSREVENUE.rdt_nrp_swodf_fourth_join_case("rdt_nrp_swodf_fourth_join"))
        rdt_nrp_swodf_fourth_join_case.createOrReplaceTempView("rdt_nrp_swodf_fourth_join_case")
        logger.info(f"Function: rdt_nrp_swodf_fourth_join_case | Executed")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_case | Row show: {rdt_nrp_swodf_fourth_join_case.show(5)}")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_case | Row Count: {rdt_nrp_swodf_fourth_join_case.count()}")
        spark.catalog.dropTempView("rdt_nrp_swodf_campaign_codes")
        rdt_nrp_swodf_fourth_join_case.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_fourth_join_case/')
        
        rdt_nrp_swodf_fourth_join_rename = spark.sql(DSREVENUE.rdt_nrp_swodf_fourth_join_rename("rdt_nrp_swodf_fourth_join_case"))
        rdt_nrp_swodf_fourth_join_rename.createOrReplaceTempView("rdt_nrp_swodf_fourth_join_rename")
        logger.info(f"Function: rdt_nrp_swodf_fourth_join_rename | Executed")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_rename | Row show: {rdt_nrp_swodf_fourth_join_rename.show(5)}")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_rename | Row Count: {rdt_nrp_swodf_fourth_join_rename.count()}")
        rdt_nrp_swodf_fourth_join.unpersist()
        spark.catalog.dropTempView("rdt_nrp_swodf_offers")
        spark.catalog.dropTempView("rdt_nrp_swodf_fourth_join_case")
        rdt_nrp_swodf_fourth_join_rename.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_fourth_join_rename/')
        
        rdt_nrp_swodf_fourth_join_groupby = spark.sql(DSREVENUE.rdt_nrp_swodf_fourth_join_groupby("rdt_nrp_swodf_fourth_join_rename"))
        rdt_nrp_swodf_fourth_join_groupby.createOrReplaceTempView("rdt_nrp_swodf_fourth_join_groupby")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_groupby | Row show: {rdt_nrp_swodf_fourth_join_groupby.show(5)}")
        logger.info(f"Function: rdt_nrp_swodf_fourth_join_groupby | Executed")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_groupby | Row Count: {rdt_nrp_swodf_fourth_join_groupby.count()}")
        spark.catalog.dropTempView("rdt_nrp_swodf_fourth_join")
        spark.catalog.dropTempView("rdt_nrp_swodf_fourth_join_rename")
        rdt_nrp_swodf_fourth_join_groupby.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_fourth_join_groupby/')
        
        rdt_nrp_swodf_fourth_join_groupby_case = spark.sql(DSREVENUE.rdt_nrp_swodf_fourth_join_groupby_case("rdt_nrp_swodf_fourth_join_groupby"))
        rdt_nrp_swodf_fourth_join_groupby_case.createOrReplaceTempView("rdt_nrp_swodf_fourth_join_groupby_case")
        logger.info(f"Function: rdt_nrp_swodf_fourth_join_groupby_case | Executed")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_groupby_case | Row show: {rdt_nrp_swodf_fourth_join_groupby_case.show(5)}")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_groupby_case | Row Count: {rdt_nrp_swodf_fourth_join_groupby_case.count()}")
        spark.catalog.dropTempView("rdt_nrp_swodf_mirations")
        rdt_nrp_swodf_fourth_join_groupby_case.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_fourth_join_groupby_case/')
        
        # rdt_nrp_swodf_fourth_join_groupby_case_filter
        rdt_nrp_swodf_fourth_join_groupby_case_filter = spark.sql(DSREVENUE.rdt_nrp_swodf_fourth_join_groupby_case_filter("rdt_nrp_swodf_fourth_join_groupby_case"))
        rdt_nrp_swodf_fourth_join_groupby_case_filter.createOrReplaceTempView("rdt_nrp_swodf_fourth_join_groupby_case_filter")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_groupby_case_filter | Row show: {rdt_nrp_swodf_fourth_join_groupby_case_filter.show(5)}")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_groupby_case_filter | Row Count: {rdt_nrp_swodf_fourth_join_groupby_case_filter.count()}")
        rdt_nrp_swodf_fourth_join_groupby_case_filter.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_fourth_join_groupby_case_filter/')
        
        # rdt_nrp_swodf_fourth_join_groupby_case_filter_rename
        rdt_nrp_swodf_fourth_join_groupby_case_filter_rename = spark.sql(DSREVENUE.rdt_nrp_swodf_fourth_join_groupby_case_filter_rename("rdt_nrp_swodf_fourth_join_groupby_case_filter"))
        rdt_nrp_swodf_fourth_join_groupby_case_filter_rename.createOrReplaceTempView("rdt_nrp_swodf_fourth_join_groupby_case_filter_rename")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_groupby_case_filter_rename | Row show: {rdt_nrp_swodf_fourth_join_groupby_case_filter_rename.show(5)}")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_groupby_case_filter_rename | Row Count: {rdt_nrp_swodf_fourth_join_groupby_case_filter_rename.count()}")
        rdt_nrp_swodf_fourth_join_groupby.unpersist()
        spark.catalog.dropTempView("rdt_nrp_swodf_fourth_join_groupby")
        spark.catalog.dropTempView("rdt_nrp_swodf_fourth_join_groupby_case")
        rdt_nrp_swodf_fourth_join_groupby_case_filter_rename.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_fourth_join_groupby_case_filter_rename/')
        
        # rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter
        rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter = spark.sql(DSREVENUE.rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter("rdt_nrp_swodf_fourth_join_groupby_case_filter_rename"))
        rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter.createOrReplaceTempView("rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter | Row show: {rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter.show(5)}")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter | Row Count: {rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter.count()}")
        spark.catalog.dropTempView("rdt_nrp_swodf_fourth_join_groupby_case_filter")
        rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter/')
        
        # rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod
        rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod = spark.sql(DSREVENUE.rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod("rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter"))
        rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod.createOrReplaceTempView("rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod")
        # logger.info(f"Function: rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod | Row show: {rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod.show(5)}")
        logger.info(f"Function: rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod | Row Count: {rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod.count()}")
        spark.catalog.dropTempView("rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter")
        rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod/')
        
        creates_new_te_segment_field_split = spark.sql(DSREVENUE2.creates_new_te_segment_field_split("rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod"))
        creates_new_te_segment_field_split.createOrReplaceTempView("creates_new_te_segment_field_split")
        logger.info(f"Function: creates_new_te_segment_field_split | Executed")
        # logger.info(f"Function: creates_new_te_segment_field_split | Row show: {creates_new_te_segment_field_split.show(5)}")
        # logger.info(f"Function: creates_new_te_segment_field_split | Row Count: {creates_new_te_segment_field_split.count()}")
        spark.catalog.dropTempView("rdt_nrp_swodf_fourth_join_groupby_case_filter_rename")
        creates_new_te_segment_field_split.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'creates_new_te_segment_field_split/')
        
        creates_new_te_segment_field_split_prg = spark.sql(DSREVENUE2.creates_new_te_segment_field_split_prg("creates_new_te_segment_field_split"))
        creates_new_te_segment_field_split_prg.createOrReplaceTempView("creates_new_te_segment_field_split_prg")
        logger.info(f"Function: creates_new_te_segment_field_split_prg | Executed")
        # logger.info(f"Function: creates_new_te_segment_field_split_prg | Row show: {creates_new_te_segment_field_split_prg.show(5)}")
        # logger.info(f"Function: creates_new_te_segment_field_split_prg | Row Count: {creates_new_te_segment_field_split_prg.count()}")
        creates_new_te_segment_field_split_prg.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'creates_new_te_segment_field_split_prg/')
        
        creates_new_te_segment_field_split_prg1 = spark.sql(DSREVENUE2.creates_new_te_segment_field_split_prg1("creates_new_te_segment_field_split_prg"))
        creates_new_te_segment_field_split_prg1.createOrReplaceTempView("creates_new_te_segment_field_split_prg1")
        # logger.info(f"Function: creates_new_te_segment_field_split_prg1 | Row show: {creates_new_te_segment_field_split_prg1.show(5)}")
        # logger.info(f"Function: creates_new_te_segment_field_split_prg1 | Row Count: {creates_new_te_segment_field_split_prg1.count()}")
        spark.catalog.dropTempView("creates_new_te_segment_field_split")
        creates_new_te_segment_field_split_prg1.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'creates_new_te_segment_field_split_prg1/')
        
        creates_new_te_segment_field_split_prg_tile = spark.sql(DSREVENUE2.creates_new_te_segment_field_split_prg_tile("creates_new_te_segment_field_split_prg1"))
        creates_new_te_segment_field_split_prg_tile.createOrReplaceTempView("creates_new_te_segment_field_split_prg_tile")
        # logger.info(f"Function: creates_new_te_segment_field_split_prg_tile | Row show: {creates_new_te_segment_field_split_prg_tile.show(5)}")
        # logger.info(f"Function: creates_new_te_segment_field_split_prg_tile | Row Count: {creates_new_te_segment_field_split_prg_tile.count()}")
        creates_new_te_segment_field_split_prg_tile.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'creates_new_te_segment_field_split_prg_tile/')
        
        creates_new_te_segment_field_split_prg_tile11 = spark.sql(DSREVENUE2.creates_new_te_segment_field_split_prg_tile11("creates_new_te_segment_field_split_prg_tile"))
        creates_new_te_segment_field_split_prg_tile11.createOrReplaceTempView("creates_new_te_segment_field_split_prg_tile11")
        logger.info(f"Function: creates_new_te_segment_field_split_prg_tile11 | Executed")
        # logger.info(f"Function: creates_new_te_segment_field_split_prg_tile11 | Row show: {creates_new_te_segment_field_split_prg_tile11.show(5)}")
        # logger.info(f"Function: creates_new_te_segment_field_split_prg_tile11 | Row Count: {creates_new_te_segment_field_split_prg_tile11.count()}")
        spark.catalog.dropTempView("creates_new_te_segment_field_split_prg")
        spark.catalog.dropTempView("creates_new_te_segment_field_split_prg1")
        creates_new_te_segment_field_split_prg_tile11.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'creates_new_te_segment_field_split_prg_tile11/')
        
        creates_new_te_segment_field_split_prg_tile1 = spark.sql(DSREVENUE2.creates_new_te_segment_field_split_prg_tile1("creates_new_te_segment_field_split_prg_tile11"))
        creates_new_te_segment_field_split_prg_tile1.createOrReplaceTempView("creates_new_te_segment_field_split_prg_tile1")
        # logger.info(f"Function: creates_new_te_segment_field_split_prg_tile1 | Row show: {creates_new_te_segment_field_split_prg_tile1.show(5)}")
        logger.info(f"Function: creates_new_te_segment_field_split_prg_tile1 | Executed")
        # logger.info(f"Function: creates_new_te_segment_field_split_prg_tile1 | Row Count: {creates_new_te_segment_field_split_prg_tile1.count()}")
        creates_new_te_segment_field_split_prg_tile1.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'creates_new_te_segment_field_split_prg_tile1/')
        
        creates_new_te_segment_final_join = spark.sql(DSREVENUE2.creates_new_te_segment_final_join("rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod", "creates_new_te_segment_field_split_prg_tile1"))
        creates_new_te_segment_final_join.createOrReplaceTempView("creates_new_te_segment_final_join")
        # logger.info(f"Function: creates_new_te_segment_final_join | Row show: {creates_new_te_segment_final_join.show(5)}")
        logger.info(f"Function: creates_new_te_segment_final_join | Executed")
        creates_new_te_segment_final_join.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'creates_new_te_segment_final_join/')
        
        rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod.unpersist()
        spark.catalog.dropTempView("rdt_nrp_swodf_fourth_join_groupby_case_filter_rename_parse_delimeter_mod")
        spark.catalog.dropTempView("creates_new_te_segment_field_split_prg_tile")
        
        
        mdu_qc_flag = spark.sql(DSREVENUE2.mdu_qc_flag())
        mdu_qc_flag.createOrReplaceTempView("mdu_qc_flag")
        # logger.info(f"Function: mdu_qc_flag | Row show: {mdu_qc_flag.show(5)}")
        # logger.info(f"Function: mdu_qc_flag | Row Count: {mdu_qc_flag.count()}")
        mdu_qc_flag.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'mdu_qc_flag/')
        
        mdu_qc_flag_schd = spark.sql(DSREVENUE2.mdu_qc_flag_schd())
        mdu_qc_flag_schd.createOrReplaceTempView("mdu_qc_flag_schd")
        # logger.info(f"Function: mdu_qc_flag_schd | Row show: {mdu_qc_flag_schd.show(5)}")
        logger.info(f"Function: mdu_qc_flag_schd | Row Count: {mdu_qc_flag_schd.count()}")
        spark.catalog.dropTempView("creates_new_te_segment_field_split_prg_tile11")
        mdu_qc_flag_schd.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'mdu_qc_flag_schd/')
        
        # mdu_qc_flag_schd_first_join = spark.sql(DSREVENUE2.mdu_qc_flag_schd_first_join("mdu_qc_flag_test", "mdu_qc_flag_schd"))
        mdu_qc_flag_schd_first_join = spark.sql(DSREVENUE2.mdu_qc_flag_schd_first_join("mdu_qc_flag", "mdu_qc_flag_schd"))
        mdu_qc_flag_schd_first_join.createOrReplaceTempView("mdu_qc_flag_schd_first_join")
        # logger.info(f"Function: mdu_qc_flag_schd_first_join | Row show: {mdu_qc_flag_schd_first_join.show(5)}")
        # logger.info(f"Function: mdu_qc_flag_schd_first_join | Row Count: {mdu_qc_flag_schd_first_join.count()}")
        spark.catalog.dropTempView("mdu_qc_flag")
        mdu_qc_flag_schd_first_join.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'mdu_qc_flag_schd_first_join/')
        
        mdu_qc_flag_schd_first_join_rename = spark.sql(DSREVENUE2.mdu_qc_flag_schd_first_join_rename("mdu_qc_flag_schd_first_join"))
        mdu_qc_flag_schd_first_join_rename.createOrReplaceTempView("mdu_qc_flag_schd_first_join_rename")
        # logger.info(f"Function: mdu_qc_flag_schd_first_join_rename | Row show: {mdu_qc_flag_schd_first_join_rename.show(5)}")
        # logger.info(f"Function: mdu_qc_flag_schd_first_join_rename | Row Count: {mdu_qc_flag_schd_first_join_rename.count()}")
        spark.catalog.dropTempView("mdu_qc_flag_schd")
        mdu_qc_flag_schd_first_join_rename.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'mdu_qc_flag_schd_first_join_rename/')
        
        mdu_qc_flag_schd_first_join_rename_groupby = spark.sql(DSREVENUE2.mdu_qc_flag_schd_first_join_rename_groupby("mdu_qc_flag_schd_first_join_rename"))
        mdu_qc_flag_schd_first_join_rename_groupby.createOrReplaceTempView("mdu_qc_flag_schd_first_join_rename_groupby")
        # logger.info(f"Function: mdu_qc_flag_schd_first_join_rename_groupby | Row show: {mdu_qc_flag_schd_first_join_rename_groupby.show(5)}")
        # logger.info(f"Function: mdu_qc_flag_schd_first_join_rename_groupby | Row Count: {mdu_qc_flag_schd_first_join_rename_groupby.count()}")
        mdu_qc_flag_schd_first_join_rename_groupby.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'mdu_qc_flag_schd_first_join_rename_groupby/')
        
        mdu_qc_flag_schd_final_join = spark.sql(DSREVENUE2.mdu_qc_flag_schd_final_join("creates_new_te_segment_final_join", "mdu_qc_flag_schd_first_join_rename_groupby"))
        mdu_qc_flag_schd_final_join.createOrReplaceTempView("mdu_qc_flag_schd_final_join")
        # logger.info(f"Function: mdu_qc_flag_schd_final_join | Row show: {mdu_qc_flag_schd_final_join.show(5)}")
        # logger.info(f"Function: mdu_qc_flag_schd_final_join | Row Count: {mdu_qc_flag_schd_final_join.count()}")
        creates_new_te_segment_field_split_prg_tile1.unpersist()
        spark.catalog.dropTempView("creates_new_te_segment_field_split_prg_tile1")
        mdu_qc_flag_schd_final_join.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'mdu_qc_flag_schd_final_join/')
        
        add_mdu_connect_flag_first = spark.sql(DSREVENUE3.add_mdu_connect_flag_first())
        add_mdu_connect_flag_first.createOrReplaceTempView("add_mdu_connect_flag_first")
        # logger.info(f"Function: add_mdu_connect_flag_first | Row show: {add_mdu_connect_flag_first.show(5)}")
        # logger.info(f"Function: add_mdu_connect_flag_first | Row Count: {add_mdu_connect_flag_first.count()}")
        spark.catalog.dropTempView("mdu_qc_flag_schd_first_join_rename_groupby")
        spark.catalog.dropTempView("mdu_qc_flag_schd_first_join_rename")
        add_mdu_connect_flag_first.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'add_mdu_connect_flag_first/')
        
        add_mdu_connect_flag_first_join = spark.sql(DSREVENUE3.add_mdu_connect_flag_first_join("mdu_qc_flag_schd_final_join", "add_mdu_connect_flag_first"))
        add_mdu_connect_flag_first_join.createOrReplaceTempView("add_mdu_connect_flag_first_join")
        # logger.info(f"Function: add_mdu_connect_flag_first_join | Row show: {add_mdu_connect_flag_first_join.show(5)}")
        # logger.info(f"Function: add_mdu_connect_flag_first_join | Row Count: {add_mdu_connect_flag_first_join.count()}")
        mdu_qc_flag_schd_final_join.unpersist()
        spark.catalog.dropTempView("mdu_qc_flag_schd_final_join")
        spark.catalog.dropTempView("mdu_qc_flag_schd_first_join")
        add_mdu_connect_flag_first_join.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'add_mdu_connect_flag_first_join/')
        
        add_mdu_connect_flag_second = spark.sql(DSREVENUE3.add_mdu_connect_flag_second())
        add_mdu_connect_flag_second.createOrReplaceTempView("add_mdu_connect_flag_second")
        # logger.info(f"Function: add_mdu_connect_flag_second | Row show: {add_mdu_connect_flag_second.show(5)}")
        # logger.info(f"Function: add_mdu_connect_flag_second | Row Count: {add_mdu_connect_flag_second.count()}")
        add_mdu_connect_flag_second.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'add_mdu_connect_flag_second/')
        
        add_mdu_connect_flag_second_join = spark.sql(DSREVENUE3.add_mdu_connect_flag_second_join("add_mdu_connect_flag_first_join", "add_mdu_connect_flag_second"))
        add_mdu_connect_flag_second_join.createOrReplaceTempView("add_mdu_connect_flag_second_join")
        # logger.info(f"Function: add_mdu_connect_flag_second_join | Row show: {add_mdu_connect_flag_second_join.show(5)}")
        # logger.info(f"Function: add_mdu_connect_flag_second_join | Row Count: {add_mdu_connect_flag_second_join.count()}")
        add_mdu_connect_flag_first_join.unpersist()
        spark.catalog.dropTempView("add_mdu_connect_flag_first_join")
        spark.catalog.dropTempView("add_mdu_connect_flag_first")
        add_mdu_connect_flag_second_join.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'add_mdu_connect_flag_second_join/')
        
        add_mdu_connect_flag_third = spark.sql(DSREVENUE3.add_mdu_connect_flag_third())
        add_mdu_connect_flag_third.createOrReplaceTempView("add_mdu_connect_flag_third")
        # logger.info(f"Function: add_mdu_connect_flag_third | Row show: {add_mdu_connect_flag_third.show(5)}")
        # logger.info(f"Function: add_mdu_connect_flag_third | Row Count: {add_mdu_connect_flag_third.count()}")
        spark.catalog.dropTempView("add_mdu_connect_flag_second")
        add_mdu_connect_flag_third.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'add_mdu_connect_flag_third/')
        
        add_mdu_connect_flag_third_join = spark.sql(DSREVENUE3.add_mdu_connect_flag_third_join("add_mdu_connect_flag_second_join", "add_mdu_connect_flag_third"))
        add_mdu_connect_flag_third_join.createOrReplaceTempView("add_mdu_connect_flag_third_join")
        # logger.info(f"Function: add_mdu_connect_flag_third_join | Row show: {add_mdu_connect_flag_third_join.show(5)}")
        # logger.info(f"Function: add_mdu_connect_flag_third_join | Row Count: {add_mdu_connect_flag_third_join.count()}")
        add_mdu_connect_flag_third_join.coalesce(1).write.format("parquet").option("header", "true").mode("overwrite").save(output_path+'add_mdu_connect_flag_third_join/')
        add_mdu_connect_flag_second_join.unpersist()
        spark.catalog.dropTempView("add_mdu_connect_flag_second_join")
        
        add_mdu_connect_flag_fourth = spark.sql(DSREVENUE3.add_mdu_connect_flag_fourth())
        add_mdu_connect_flag_fourth.createOrReplaceTempView("add_mdu_connect_flag_fourth")
        # logger.info(f"Function: add_mdu_connect_flag_fourth | Row show: {add_mdu_connect_flag_fourth.show(5)}")
        # logger.info(f"Function: add_mdu_connect_flag_fourth | Row Count: {add_mdu_connect_flag_fourth.count()}")
        spark.catalog.dropTempView("add_mdu_connect_flag_third")
        add_mdu_connect_flag_fourth.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'add_mdu_connect_flag_fourth/')
        
        add_mdu_connect_flag_fourth_join = spark.sql(DSREVENUE3.add_mdu_connect_flag_fourth_join("add_mdu_connect_flag_third_join", "add_mdu_connect_flag_fourth"))
        add_mdu_connect_flag_fourth_join.createOrReplaceTempView("add_mdu_connect_flag_fourth_join")
        logger.info(f"Function: add_mdu_connect_flag_fourth_join | Executed")
        # logger.info(f"Function: add_mdu_connect_flag_fourth_join | Row show: {add_mdu_connect_flag_fourth_join.show(5)}")
        # logger.info(f"Function: add_mdu_connect_flag_fourth_join | Row Count: {add_mdu_connect_flag_fourth_join.count()}")
        add_mdu_connect_flag_third_join.unpersist()
        spark.catalog.dropTempView("add_mdu_connect_flag_third_join")
        add_mdu_connect_flag_fourth_join.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'add_mdu_connect_flag_fourth_join/')
        
        add_dwelling_type_agent_metric = spark.sql(DSREVENUE3.add_dwelling_type_agent_metric())
        add_dwelling_type_agent_metric.createOrReplaceTempView("add_dwelling_type_agent_metric")
        # logger.info(f"Function: add_dwelling_type_agent_metric | Row show: {add_dwelling_type_agent_metric.show(5)}")
        # logger.info(f"Function: add_dwelling_type_agent_metric | Row Count: {add_dwelling_type_agent_metric.count()}")
        spark.catalog.dropTempView("add_mdu_connect_flag_fourth")
        add_dwelling_type_agent_metric.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'add_dwelling_type_agent_metric/')
        
        add_dwelling_type_agent_dwelling_type_dim = spark.sql(DSREVENUE3.add_dwelling_type_agent_dwelling_type_dim())
        add_dwelling_type_agent_dwelling_type_dim.createOrReplaceTempView("add_dwelling_type_agent_dwelling_type_dim")
        # logger.info(f"Function: add_dwelling_type_agent_dwelling_type_dim | Row show: {add_dwelling_type_agent_dwelling_type_dim.show(5)}")
        # logger.info(f"Function: add_dwelling_type_agent_dwelling_type_dim | Row Count: {add_dwelling_type_agent_dwelling_type_dim.count()}")
        add_dwelling_type_agent_dwelling_type_dim.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'add_dwelling_type_agent_dwelling_type_dim/')
        
        add_dwelling_type_first_join = spark.sql(DSREVENUE3.add_dwelling_type_first_join("add_mdu_connect_flag_fourth_join","add_dwelling_type_agent_metric"))
        add_dwelling_type_first_join.createOrReplaceTempView("add_dwelling_type_first_join")
        logger.info(f"Function: add_dwelling_type_first_join | Executed")
        # logger.info(f"Function: add_dwelling_type_first_join | Row show: {add_dwelling_type_first_join.show(5)}")
        # logger.info(f"Function: add_dwelling_type_first_join | Row Count: {add_dwelling_type_first_join.count()}")
        add_mdu_connect_flag_fourth_join.unpersist()
        spark.catalog.dropTempView("add_mdu_connect_flag_fourth_join")
        add_dwelling_type_first_join.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'add_dwelling_type_first_join/')
        
        add_dwelling_type_second_join = spark.sql(DSREVENUE3.add_dwelling_type_second_join("add_dwelling_type_first_join","add_dwelling_type_agent_dwelling_type_dim"))
        add_dwelling_type_second_join.createOrReplaceTempView("add_dwelling_type_second_join")
        # logger.info(f"Function: add_dwelling_type_second_join | Row show: {add_dwelling_type_second_join.show(5)}")
        # logger.info(f"Function: add_dwelling_type_second_join | Row Count: {add_dwelling_type_second_join.count()}")
        spark.catalog.dropTempView("add_dwelling_type_agent_metric")
        spark.catalog.dropTempView("add_dwelling_type_first_join")
        add_dwelling_type_second_join.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'add_dwelling_type_second_join/')
        
        add_dwelling_type_second_join_filter = spark.sql(DSREVENUE3.add_dwelling_type_second_join_filter("add_dwelling_type_second_join"))
        add_dwelling_type_second_join_filter.createOrReplaceTempView("add_dwelling_type_second_join_filter")
        # logger.info(f"Function: add_dwelling_type_second_join_filter | Row show: {add_dwelling_type_second_join_filter.show(5)}")
        logger.info(f"Function: add_dwelling_type_second_join_filter | Executed")
        # logger.info(f"Function: add_dwelling_type_second_join_filter | Row Count: {add_dwelling_type_second_join_filter.count()}")
        spark.catalog.dropTempView("add_dwelling_type_second_join")
        add_dwelling_type_second_join_filter.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'add_dwelling_type_second_join_filter/')
        
        chsi_go_tier = spark.sql(DSREVENUE4.chsi_go_tier("add_dwelling_type_second_join_filter"))
        chsi_go_tier.createOrReplaceTempView("chsi_go_tier")
        logger.info(f"Function: chsi_go_tier | Executed")
        # logger.info(f"Function: chsi_go_tier | Row show: {chsi_go_tier.show(5)}")
        # logger.info(f"Function: chsi_go_tier | Row Count: {chsi_go_tier.count()}")
        add_dwelling_type_second_join_filter.unpersist()
        spark.catalog.dropTempView("add_dwelling_type_second_join_filter")
        chsi_go_tier.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'chsi_go_tier/')
        
        chsi_go_tier_filter = spark.sql(DSREVENUE4.chsi_go_tier_filter("chsi_go_tier"))
        chsi_go_tier_filter.createOrReplaceTempView("chsi_go_tier_filter")
        logger.info(f"Function: chsi_go_tier_filter | Executed")
        # logger.info(f"Function: chsi_go_tier_filter | Row show: {chsi_go_tier_filter.show(5)}")
        # logger.info(f"Function: chsi_go_tier_filter | Row Count: {chsi_go_tier_filter.count()}")
        spark.catalog.dropTempView("add_dwelling_type_agent_dwelling_type_dim")
        chsi_go_tier_filter.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'chsi_go_tier_filter/')
        
        chsi_go_tier_filter2 = spark.sql(DSREVENUE4.chsi_go_tier_filter2("chsi_go_tier_filter"))
        chsi_go_tier_filter2.createOrReplaceTempView("chsi_go_tier_filter2")
        logger.info(f"Function: chsi_go_tier_filter2 | Executed")
        # logger.info(f"Function: chsi_go_tier_filter2 | Row show: {chsi_go_tier_filter2.show(5)}")
        # logger.info(f"Function: chsi_go_tier_filter2 | Row Count: {chsi_go_tier_filter2.count()}")
        # chsi_go_tier_filter2.coalesce(1).write.format("csv").option("header", "true").mode("overwrite").save(output_path+'chsi_go_tier_filter2/')
        spark.catalog.dropTempView("chsi_go_tier")
        chsi_go_tier_filter2.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'chsi_go_tier_filter2/')
        
        # ds_revenue_remove_last35days = spark.sql(DSREVENUE4.ds_revenue_remove_last35days())
        ds_revenue_remove_last35days = spark.sql(DSREVENUE4.ds_revenue_remove_last35days(180))
        ds_revenue_remove_last35days.createOrReplaceTempView("ds_revenue_remove_last35days")
        logger.info(f"Function: ds_revenue_remove_last35days | Executed")
        # logger.info(f"Function: ds_revenue_remove_last35days | Row show: {ds_revenue_remove_last35days.show(5)}")
        # logger.info(f"Function: ds_revenue_remove_last35days | Row Count: {ds_revenue_remove_last35days.count()}")
        #limit records
        ds_revenue_remove_last35days.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'ds_revenue_remove_last35days/')
        
        chsi_go_tier_union = spark.sql(DSREVENUE4.chsi_go_tier_union("ds_revenue_remove_last35days","chsi_go_tier_filter2"))
        chsi_go_tier_union.persist(StorageLevel.MEMORY_AND_DISK)
        chsi_go_tier_union.createOrReplaceTempView("chsi_go_tier_union")
        chsi_go_tier_union.printSchema()
        logger.info(f"Function: chsi_go_tier_union | Executed")
        chsi_go_tier_union = chsi_go_tier_union.withColumn("Activity Base", col("Activity Base").cast("string"))
        # logger.info(f"Function: chsi_go_tier_union | Row show: {chsi_go_tier_union.show(5)}")
        # logger.info(f"Function: chsi_go_tier_union | Row Count: {chsi_go_tier_union.count()}")
        chsi_go_tier_union.coalesce(1).write.format("parquet").option("header", "true").mode("overwrite").save(output_path+'chsi_go_tier_union/')
        spark.catalog.dropTempView("chsi_go_tier_filter")
        
        ds_revenue_remove_last35days.unpersist()
        spark.catalog.dropTempView("ds_revenue_remove_last35days")
        
        apply_further_logic = spark.sql(DSREVENUE4.apply_further_logic())
        apply_further_logic.createOrReplaceTempView("apply_further_logic")
        logger.info(f"Function: apply_further_logic | Executed")
        # logger.info(f"Function: apply_further_logic | Row show: {apply_further_logic.show(5)}")
        # logger.info(f"Function: apply_further_logic | Row Count: {apply_further_logic.count()}")
        apply_further_logic.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'apply_further_logic/')
        apply_further_logic.cache()
        
        
        apply_further_logic_group1 = spark.sql(DSREVENUE4.apply_further_logic_group1("apply_further_logic"))
        apply_further_logic_group1.createOrReplaceTempView("apply_further_logic_group1")
        logger.info(f"Function: apply_further_logic_group1 | Executed")
        # logger.info(f"Function: apply_further_logic_group1 | Row show: {apply_further_logic_group1.show(5)}")
        # logger.info(f"Function: apply_further_logic_group1 | Row Count: {apply_further_logic_group1.count()}")
        spark.catalog.dropTempView("chsi_go_tier_filter2")
        apply_further_logic_group1.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'apply_further_logic_group1/')
        
        apply_further_logic_group2 = spark.sql(DSREVENUE4.apply_further_logic_group2("apply_further_logic"))
        apply_further_logic_group2.createOrReplaceTempView("apply_further_logic_group2")
        logger.info(f"Function: apply_further_logic_group2 | Executed")
        # logger.info(f"Function: apply_further_logic_group2 | Row show: {apply_further_logic_group2.show(5)}")
        # logger.info(f"Function: apply_further_logic_group2 | Row Count: {apply_further_logic_group2.count()}")
        spark.catalog.dropTempView("apply_further_logic")
        apply_further_logic_group2.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'apply_further_logic_group2/')
        
        apply_further_logic_join = spark.sql(DSREVENUE4.apply_further_logic_join("apply_further_logic_group1", "apply_further_logic_group2"))
        apply_further_logic_join.createOrReplaceTempView("apply_further_logic_join")
        # logger.info(f"Function: apply_further_logic_join | Row show: {apply_further_logic_join.show(5)}")
        logger.info(f"Function: apply_further_logic_join | Executed")
        # logger.info(f"Function: apply_further_logic_join | Row Count: {apply_further_logic_join.count()}")
        spark.catalog.dropTempView("apply_further_logic_group1")
        spark.catalog.dropTempView("apply_further_logic_group2")
        apply_further_logic_join.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'apply_further_logic_join/')
        
        apply_further_logic_join_condition = spark.sql(DSREVENUE4.apply_further_logic_join_condition("apply_further_logic_join"))
        apply_further_logic_join_condition.createOrReplaceTempView("apply_further_logic_join_condition")
        # logger.info(f"Function: apply_further_logic_join_condition | Row show: {apply_further_logic_join_condition.show(5)}")
        logger.info(f"Function: apply_further_logic_join_condition | Executed")
        # logger.info(f"Function: apply_further_logic_join_condition | Row Count: {apply_further_logic_join_condition.count()}")
        # apply_further_logic_join_condition.cache()
        apply_further_logic_join_condition.persist(StorageLevel.MEMORY_AND_DISK)
        apply_further_logic.unpersist()
        spark.catalog.dropTempView("apply_further_logic")
        spark.catalog.dropTempView("apply_further_logic_join")
        apply_further_logic_join_condition.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'apply_further_logic_join_condition/')
        
        cro_eligibility = spark.sql(DSREVENUE5.cro_eligibility("chsi_go_tier_union"))
        cro_eligibility.persist(StorageLevel.MEMORY_AND_DISK)
        cro_eligibility.createOrReplaceTempView("cro_eligibility")
        logger.info(f"Function: cro_eligibility | Executed")
        cro_eligibility.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility/')
        
        cro_eligibility_cronotnull_cronotpost_cronotpre = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre("chsi_go_tier_union"))
        cro_eligibility_cronotnull_cronotpost_cronotpre.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre")
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_union = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_union("cro_eligibility","cro_eligibility_cronotnull_cronotpost_cronotpre"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_union.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_union")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_union | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_union.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_union | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_union.count()}")
        spark.catalog.dropTempView("cro_eligibility")
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_union | Executed")
        cro_eligibility_cronotnull_cronotpost_cronotpre_union.persist(StorageLevel.MEMORY_AND_DISK)
        cro_eligibility_cronotnull_cronotpost_cronotpre_union.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_cronotnull_cronotpost_cronotpre_union/')
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_join("cro_eligibility_cronotnull_cronotpost_cronotpre_union", "apply_further_logic_join_condition"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_join.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join.cache()
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join | Executed")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_join.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_join.count()}")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_cronotnull_cronotpost_cronotpre_join/')
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f1 = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f1("cro_eligibility_cronotnull_cronotpost_cronotpre_join"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f1.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f1")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f1.cache()
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f1 | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f1.show(5)}")
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f1 | Executed")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f1 | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f1.count()}")
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f2 = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f2("cro_eligibility_cronotnull_cronotpost_cronotpre_join"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f2.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f2")
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f2 | Executed")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f2.cache()
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f2 | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f2.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f2 | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f2.count()}")
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f3 = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f3("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f2"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f3.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f3")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f3.cache()
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f3 | Executed")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f3 | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f3.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f3 | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f3.count()}")
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f4 = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f4("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f2"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f4.cache()
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f4.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f4")
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f4 | Executed")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f4 | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f4.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f4 | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f4.count()}")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f2.unpersist()
        
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f2")
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f5 = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f5("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f4"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f5.cache()
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f5.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f5")
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f5 | Executed")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f5 | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f5.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f5 | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f5.count()}")
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre")
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f6 = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f6("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f4"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f6.cache()
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f6.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f6")
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f6 | Executed")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f6 | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f6.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f6 | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f6.count()}")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f4.unpersist()
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f4")
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f7 = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f7("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f5"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f7.cache()
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f7.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f7")
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f7 | Executed")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f7 | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f7.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f7 | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f7.count()}")
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f8 = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f8("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f5"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f8.cache()
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f8.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f8")
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f8 | Executed")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f8 | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f8.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f8 | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f8.count()}")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f5.unpersist()
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f5")
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f1", "cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f3","cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f7"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union")
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union | Executed")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union.persist(StorageLevel.MEMORY_AND_DISK)
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union.count()}")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f1.unpersist()
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f3.unpersist()
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f7.unpersist()
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f1")
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f3")
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f7")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union/')
        
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2 = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f8", "cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f6"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2")
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2 | Executed")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2/')
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2 | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2 | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2.count()}")
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f6.unpersist()
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f8.unpersist()
        cro_eligibility_cronotnull_cronotpost_cronotpre_join.unpersist()
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f6")
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f7")
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_f8")
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join")
        
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter1 = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter1("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter1.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter1")
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter1 | Executed")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter1 | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter1.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter1 | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter1.count()}")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter1.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter1/')
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter2 = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter2("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter1"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter2.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter2")
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter2 | Executed")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter2 | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter2.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter2 | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter2.count()}")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter2.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter2/')
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter3 = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter3("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter2"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter3.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter3")
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter3 | Executed")
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter3.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter3/')
        
        cro_eligibility_cronotnull_cropost = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cropost("chsi_go_tier_union"))
        cro_eligibility_cronotnull_cropost.createOrReplaceTempView("cro_eligibility_cronotnull_cropost")
        cro_eligibility_cronotnull_cropost.cache()
        logger.info(f"Function: cro_eligibility_cronotnull_cropost | Executed")
        # logger.info(f"Function: cro_eligibility_cronotnull_cropost | Row show: {cro_eligibility_cronotnull_cropost.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cropost | Row Count: {cro_eligibility_cronotnull_cropost.count()}")
        
        cro_eligibility_cronotnull_cronotpost_cropre = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cropre("chsi_go_tier_union"))
        cro_eligibility_cronotnull_cronotpost_cropre.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cropre")
        cro_eligibility_cronotnull_cronotpost_cropre.cache()
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cropre | Executed")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cropre | Row show: {cro_eligibility_cronotnull_cronotpost_cropre.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cropre | Row Count: {cro_eligibility_cronotnull_cronotpost_cropre.count()}")
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2")
        cro_eligibility_cronotnull_cronotpost_cropre.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_cronotnull_cronotpost_cropre/')
        
        
        cro_eligibility_limits_prepost_query = spark.sql(DSREVENUE5.cro_eligibility_limits_prepost_query("cro_eligibility_cronotnull_cropost", "cro_eligibility_cronotnull_cronotpost_cropre","cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter3"))
        cro_eligibility_limits_prepost_query.persist(StorageLevel.MEMORY_AND_DISK)
        cro_eligibility_limits_prepost_query.createOrReplaceTempView("cro_eligibility_limits_prepost_query")
        # logger.info(f"Function: cro_eligibility_limits_prepost_query | Row show: {cro_eligibility_limits_prepost_query.show(5)}")
        logger.info(f"Function: cro_eligibility_limits_prepost_query Executed")
        # logger.info(f"Function: cro_eligibility_limits_prepost_query | Row Count: {cro_eligibility_limits_prepost_query.count()}")
        cro_eligibility_limits_prepost_query.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_limits_prepost_query/')
        
        cro_eligibility_cronotnull_cronotpost_cropre.unpersist()
        cro_eligibility_cronotnull_cropost.unpersist()
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cropre")
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cropost")
        cro_eligibility_cronotnull_cropost.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_cronotnull_cropost/')
        
        cro_eligibility_limits_prepost_query2 = spark.sql(DSREVENUE5.cro_eligibility_limits_prepost_query2("cro_eligibility_limits_prepost_query"))
        cro_eligibility_limits_prepost_query2.createOrReplaceTempView("cro_eligibility_limits_prepost_query2")
        # logger.info(f"Function: cro_eligibility_limits_prepost_query2 | Row show: {cro_eligibility_limits_prepost_query2.show(5)}")
        logger.info(f"Function: cro_eligibility_limits_prepost_query2 Executed")
        # cro_eligibility_limits_prepost_query2.cache()
        # logger.info(f"Function: cro_eligibility_limits_prepost_query2 | Row Count: {cro_eligibility_limits_prepost_query2.count()}")
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter1")
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter2")
        spark.catalog.dropTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union2_filter3")
        cro_eligibility_limits_prepost_query2.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_limits_prepost_query2/')
        
        cro_eligibility_limits_prepost_query3 = spark.sql(DSREVENUE5.cro_eligibility_limits_prepost_query3("cro_eligibility_limits_prepost_query"))
        cro_eligibility_limits_prepost_query3.createOrReplaceTempView("cro_eligibility_limits_prepost_query3")
        logger.info(f"Function: cro_eligibility_limits_prepost_query3 Executed")
        cro_eligibility_limits_prepost_query3.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_limits_prepost_query3/')


        
        cro_eligibility_cronotnull_cronotpost_cronotpre_leftjoin = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_leftjoin("cro_eligibility_cronotnull_cronotpost_cronotpre_union", "apply_further_logic_join_condition"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_leftjoin.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_leftjoin")
        cro_eligibility_cronotnull_cronotpost_cronotpre_leftjoin.cache()
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_leftjoin Executed")
        cro_eligibility_cronotnull_cronotpost_cronotpre_leftjoin.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_cronotnull_cronotpost_cronotpre_leftjoin/')
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_notnull = spark.sql(DSREVENUE5.cro_eligibility_cronotnull_cronotpost_cronotpre_notnull("chsi_go_tier_union"))
        cro_eligibility_cronotnull_cronotpost_cronotpre_notnull.createOrReplaceTempView("cro_eligibility_cronotnull_cronotpost_cronotpre_notnull")
        cro_eligibility_cronotnull_cronotpost_cronotpre_notnull.cache()
        logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_notnull Executed")
        cro_eligibility_cronotnull_cronotpost_cronotpre_notnull.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_cronotnull_cronotpost_cronotpre_notnull/')
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_notnull | Row show: {cro_eligibility_cronotnull_cronotpost_cronotpre_notnull.show(5)}")
        # logger.info(f"Function: cro_eligibility_cronotnull_cronotpost_cronotpre_notnull | Row Count: {cro_eligibility_cronotnull_cronotpost_cronotpre_notnull.count()}")
        
        cro_eligibility_not180 = spark.sql(DSREVENUE5.cro_eligibility_not180("chsi_go_tier_union"))
        cro_eligibility_not180.createOrReplaceTempView("cro_eligibility_not180")
        # logger.info(f"Function: cro_eligibility_not180 | Row show: {cro_eligibility_not180.show(5)}")
        # logger.info(f"Function: cro_eligibility_not180 | Row Count: {cro_eligibility_not180.count()}")
        cro_eligibility_not180.cache()
        apply_further_logic_join_condition.unpersist()
        logger.info(f"Function: cro_eligibility_not180 Executed")
        cro_eligibility_not180.coalesce(1).write.format("parquet").mode("overwrite").save(output_path+'cro_eligibility_not180/')

        cro_eligibility_limits_prepost_final_union = spark.sql(DSREVENUE5.cro_eligibility_limits_prepost_final_union("cro_eligibility_cronotnull_cronotpost_cronotpre_leftjoin", "cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union", "cro_eligibility_limits_prepost_query2", "cro_eligibility_not180", "cro_eligibility_cronotnull_cronotpost_cronotpre_notnull","cro_eligibility_limits_prepost_query3"))
         
        cro_eligibility_limits_prepost_final_union.persist(StorageLevel.MEMORY_AND_DISK)
        cro_eligibility_limits_prepost_final_union.createOrReplaceTempView("cro_eligibility_limits_prepost_final_union")
        logger.info(f"Function: cro_eligibility_limits_prepost_final_union Executed")
        # logger.info(f"Function: cro_eligibility_limits_prepost_final_union | Row show: {cro_eligibility_limits_prepost_final_union.show(5)}")
        # logger.info(f"Function: cro_eligibility_limits_prepost_final_union | Row Count: {cro_eligibility_limits_prepost_final_union.count()}")
        cro_eligibility_limits_prepost_final_union = cro_eligibility_limits_prepost_final_union.withColumn("Activity Base", col("Activity Base").cast("string"))
        
        num_records = cro_eligibility_limits_prepost_final_union.count()
        target_partitions = max(1, min(150, num_records // 10))
        # chunk_size = num_records // target_partitions
        logger.info(f"Function: target_partitions | completed {num_records}")
        
        # cro_eligibility_limits_prepost_final_union pushed data to s3 for next job to process
        cro_eligibility_limits_prepost_final_union.repartition(target_partitions).write.option("useGlueParquetWriter", "true").mode("overwrite").parquet(output_path + 'cro_eligibility_limits_prepost_final_union/')
        
        
        response = glue_client.start_job_run(JobName=target_job_name)
        job_run_id = response['JobRunId']
        print(f"Triggered Glue job {target_job_name} with JobRunID: {job_run_id}")
        
        cro_eligibility_cronotnull_cronotpost_cronotpre_join_order_union.unpersist()
        
        update_log_query = f"""
                        update {database_nm}.digital_mkt_process_auditlog 
                        set process_status = 'Success', records_processed = {num_records}, process_end_dt = TIMESTAMP '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' where process_id = '5700' and process_start_dt = TIMESTAMP '{log_time}'
                    """
        update_log = QueryAthena(query=update_log_query, database=database_nm)
        update_log.run_query(False)
        
        # logger.info("Ensuring all writes are completed...")
        spark.sql("CLEAR CACHE")  # Clear any cached DataFrames
        spark.catalog.clearCache()
        
        logger.info(f" job | commit")
        job.commit()  # Mark job as successful
        return
        
    except Exception as e:
        print("Error", e)
        logger.error("An error occurred"+ str(e), exc_info=True)
        update_log_query = f"""
                        update {database_nm}.digital_mkt_process_auditlog 
                        set process_status = 'Failed', records_processed = 0, process_end_dt = TIMESTAMP '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' where process_id = '5700' and process_start_dt = TIMESTAMP '{log_time}'
                    """
        update_log = QueryAthena(query=update_log_query, database=database_nm)
        update_log.run_query(False)
        sys.exit(1)

## Starting main program
if __name__ == "__main__":
    main()
