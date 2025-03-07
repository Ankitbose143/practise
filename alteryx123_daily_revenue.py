
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
  
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
dyf = glueContext.create_dynamic_frame.from_catalog(database='database_name', table_name='table_name')
dyf.printSchema()
spark._jsc.hadoopConfiguration().set("fs.s3.useRequesterPaysHeader", "true")

# spark.sparkContext.addPyFile("s3://cci-edo-data-utils/alteryx_digital_marketing/ds_revenue/module/DSREVENUE4.py")
# spark.sparkContext.addPyFile("s3://cci-edo-data-utils/alteryx_digital_marketing/ds_revenue/module/DSREVENUE5.py")

# from DSREVENUE4 import DSREVENUE4
# from DSREVENUE5 import DSREVENUE5
query_revenue= """
        SELECT cast(a11.TIME_KEY as date),
               a12.DISPLAY_SALES_CHANNEL_GROUP AS DISPLAY_CHANNEL_GROUP_NM,
               a12.SALES_CHANNEL_NM AS SALES_CHANNEL_NM,
               a12.EMPLOYEE_TYPE_CD,
               a11.CUST_SITE_KEY AS SITE_KEY,
               a14.SITE_DESC,
               a11.CUSTOMER_SUBSTATUS_KEY,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_DISC_NET_REV_AMT ELSE NULL END) AS NRPA_DISC_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_DOWNGRADE_NET_REV_AMT ELSE NULL END) AS NRPA_DOWNGRADE_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_DOWNTIER_NET_REV_AMT ELSE NULL END) AS NRPA_DOWNTIER_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_NEW_CONN_NET_REV_AMT ELSE NULL END) AS NRPA_NEW_CONN_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_RESTART_NET_REV_AMT ELSE NULL END) AS NRPA_RESTART_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_SIDEGRADE_NET_REV_AMT ELSE NULL END) AS NRPA_SIDEGRADE_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_UPGRADE_NET_REV_AMT ELSE NULL END) AS NRPA_UPGRADE_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_UPTIER_NET_REV_AMT ELSE NULL END) AS NRPA_UPTIER_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_DISCONNECT_CNT ELSE NULL END) AS ACCT_CHG_DISC,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_DOWNGRADE_CNT ELSE NULL END) AS ACCT_CHG_DOWNGRADE,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_DOWNTIER_CNT ELSE NULL END) AS ACCT_CHG_DOWNTIER,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_NEW_CONNECT_CNT ELSE NULL END) AS ACCT_CHG_NEW_CONN,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_RESTART_CNT ELSE NULL END) AS ACCT_CHG_RESTART,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_SIDEGRADE_CNT ELSE NULL END) AS ACCT_CHG_SIDEGRADE,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_UPGRADE_CNT ELSE NULL END) AS ACCT_CHG_UPGRADE,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_UPTIER_CNT ELSE NULL END) AS ACCT_CHG_UPTIER,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_NONE_CNT ELSE NULL END) AS ACCT_CHG_NONE,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_OTHER_CNT ELSE NULL END) AS ACCT_CHG_OTHER,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_OTHER_NET_REV_AMT ELSE NULL END) AS NRPA_OTHER_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY IN (8, 9) THEN a11.NRPA_NET_REV_AMT ELSE NULL END) AS NRPA_TRANSFER_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY IN (8) THEN a11.ACCT_CHANGE_CNT ELSE NULL END) AS ACCT_CHG_TRANSFER,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY IN (9) THEN a11.ACCT_CHANGE_CNT ELSE NULL END) AS ACCT_CHG_E_TRANSFER,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (9) THEN a11.ACCT_CHANGE_CNT ELSE NULL END) AS ACCT_CHG,
               SUM(a11.NRPA_NET_REV_AMT) AS NRPA_NET_REV
        FROM MSADMIN.CS_AGENT_CUSTOMER_SUM a11
        JOIN MSADMIN.CS_EMPLOYEE_TYPE_CD_XREF a12 
        ON (a11.SLS_CHANNEL_EMPLOYEE_TYPE_CD = a12.EMPLOYEE_TYPE_CD AND cast(a11.TIME_KEY as date)= cast(a12.TIME_KEY as date))
        JOIN EDW.TIME_DIM a13 
        ON (cast(a11.TIME_KEY as date) = cast(a13.TIME_KEY as date))
        JOIN SIW.DIM_SITE a14 
        ON (a11.CUST_SITE_KEY = a14.SITE_KEY)
        WHERE cast(a11.TIME_KEY as date) BETWEEN 
        TO_DATE(DATE_FORMAT(CURRENT_DATE - INTERVAL 36 DAY, 'dd-MM-yyyy'), 'dd-MM-yyyy') 
        AND 
        TO_DATE(DATE_FORMAT(CURRENT_DATE - INTERVAL 1 DAY, 'dd-MM-yyyy'), 'dd-MM-yyyy')
        GROUP BY cast(a11.TIME_KEY as date),
                 a12.DISPLAY_SALES_CHANNEL_GROUP,
                 a12.SALES_CHANNEL_NM,
                 a12.EMPLOYEE_TYPE_CD,
                 a11.CUST_SITE_KEY,
                 a14.SITE_DESC,
                 a11.CUSTOMER_SUBSTATUS_KEY"""
    
    
    
# edw_join_df = createTempView(spark, tmpview_name='query1', data_query=query)
# WHERE
edw_join_df = spark.sql(query_revenue)
print(edw_join_df.count())
edw_join_df.printSchema()
edw_join_df.show(5)
edw_join_df.createOrReplaceTempView("revenue")
# revenue.show(5)
# # print(revenue)
query_aca= """
        SELECT cast(a11.TIME_KEY as date),
               a12.DISPLAY_SALES_CHANNEL_GROUP AS DISPLAY_CHANNEL_GROUP_NM,
               a12.SALES_CHANNEL_NM AS SALES_CHANNEL_NM,
               a12.EMPLOYEE_TYPE_CD,
               a11.CUST_SITE_KEY AS SITE_KEY,
               a14.SITE_DESC,
               a11.CUSTOMER_SUBSTATUS_KEY,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_DISC_NET_REV_AMT ELSE NULL END) AS NRPA_DISC_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_DOWNGRADE_NET_REV_AMT ELSE NULL END) AS NRPA_DOWNGRADE_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_DOWNTIER_NET_REV_AMT ELSE NULL END) AS NRPA_DOWNTIER_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_NEW_CONN_NET_REV_AMT ELSE NULL END) AS NRPA_NEW_CONN_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_RESTART_NET_REV_AMT ELSE NULL END) AS NRPA_RESTART_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_SIDEGRADE_NET_REV_AMT ELSE NULL END) AS NRPA_SIDEGRADE_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_UPGRADE_NET_REV_AMT ELSE NULL END) AS NRPA_UPGRADE_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_UPTIER_NET_REV_AMT ELSE NULL END) AS NRPA_UPTIER_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_DISCONNECT_CNT ELSE NULL END) AS ACCT_CHG_DISC,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_DOWNGRADE_CNT ELSE NULL END) AS ACCT_CHG_DOWNGRADE,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_DOWNTIER_CNT ELSE NULL END) AS ACCT_CHG_DOWNTIER,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_NEW_CONNECT_CNT ELSE NULL END) AS ACCT_CHG_NEW_CONN,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_RESTART_CNT ELSE NULL END) AS ACCT_CHG_RESTART,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_SIDEGRADE_CNT ELSE NULL END) AS ACCT_CHG_SIDEGRADE,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_UPGRADE_CNT ELSE NULL END) AS ACCT_CHG_UPGRADE,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_UPTIER_CNT ELSE NULL END) AS ACCT_CHG_UPTIER,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_NONE_CNT ELSE NULL END) AS ACCT_CHG_NONE,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.ACCT_CHANGE_OTHER_CNT ELSE NULL END) AS ACCT_CHG_OTHER,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (8, 9) THEN a11.NRPA_OTHER_NET_REV_AMT ELSE NULL END) AS NRPA_OTHER_NET_REV,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY IN (8, 9) THEN a11.NRPA_NET_REV_AMT ELSE NULL END) AS NRPA_TRANSFER_NET_REV,               
               SUM((Case when a11.CUSTOMER_SUBSTATUS_KEY in (8,9) then a11.ACCT_CHANGE_CNT else NULL end))  ACCT_CHG_TRANSFER,
               SUM(CASE WHEN a11.CUSTOMER_SUBSTATUS_KEY NOT IN (9) THEN a11.ACCT_CHANGE_CNT ELSE NULL END) AS ACCT_CHG,
               SUM(a11.NRPA_NET_REV_AMT) AS NRPA_NET_REV
        FROM MSADMIN.CS_AGENT_CUSTOMER_SUM a11
        JOIN MSADMIN.CS_EMPLOYEE_TYPE_CD_XREF a12 
        ON (a11.SLS_CHANNEL_EMPLOYEE_TYPE_CD = a12.EMPLOYEE_TYPE_CD AND cast(a11.TIME_KEY as date)= cast(a12.TIME_KEY as date))
        JOIN EDW.TIME_DIM a13 
        ON (cast(a11.TIME_KEY as date) = cast(a13.TIME_KEY as date))
        JOIN SIW.DIM_SITE a14 
        ON (a11.CUST_SITE_KEY = a14.SITE_KEY)
        WHERE cast(a11.TIME_KEY as date) BETWEEN 
        TO_DATE(DATE_FORMAT(CURRENT_DATE - INTERVAL 36 DAY, 'dd-MM-yyyy'), 'dd-MM-yyyy') 
        AND 
        TO_DATE(DATE_FORMAT(CURRENT_DATE - INTERVAL 1 DAY, 'dd-MM-yyyy'), 'dd-MM-yyyy')
        GROUP BY cast(a11.TIME_KEY as date),
                 a12.DISPLAY_SALES_CHANNEL_GROUP,
                 a12.SALES_CHANNEL_NM,
                 a12.EMPLOYEE_TYPE_CD,
                 a11.CUST_SITE_KEY,
                 a14.SITE_DESC,
                 a11.CUSTOMER_SUBSTATUS_KEY"""
    
    
    
# edw_join_df = createTempView(spark, tmpview_name='query1', data_query=query)
# WHERE
edw_join_df = spark.sql(query_aca)
print(edw_join_df.count())
edw_join_df.printSchema()
edw_join_df.show(5)
edw_join_df.createOrReplaceTempView("aca")
# aca.show(5)
# # print(revenue)
# query1 = """SELECT DISTINCT cast(a11.TIME_KEY as date)
# FROM MSADMIN.CS_AGENT_CUSTOMER_SUM a11
# WHERE cast(a11.TIME_KEY as date) BETWEEN 
# TO_DATE(DATE_FORMAT(CURRENT_DATE - INTERVAL 36 DAY, 'dd-MM-yyyy'), 'dd-MM-yyyy') 
# AND 
# TO_DATE(DATE_FORMAT(CURRENT_DATE - INTERVAL 1 DAY, 'dd-MM-yyyy'), 'dd-MM-yyyy')
# LIMIT 10;"""
# edw_join_df = spark.sql(query1)
# print(edw_join_df.count())
# edw_join_df.printSchema()
# edw_join_df.show(5)
# edw_join_df.createOrReplaceTempView("revenue1")
# query2 = """SELECT COUNT(*)
# FROM MSADMIN.CS_AGENT_CUSTOMER_SUM a11
# JOIN MSADMIN.CS_EMPLOYEE_TYPE_CD_XREF a12 
# ON (a11.SLS_CHANNEL_EMPLOYEE_TYPE_CD = a12.EMPLOYEE_TYPE_CD)
# WHERE cast(a11.TIME_KEY as date) BETWEEN 
#     date_sub(current_date(), 36) 
#     AND date_sub(current_date(), 1)

# AND cast(a11.TIME_KEY as date) = cast(a12.TIME_KEY as date);"""
# edw_join_df = spark.sql(query2)
# print(edw_join_df.count())
# edw_join_df.printSchema()
# edw_join_df.show(5)
# edw_join_df.createOrReplaceTempView("revenue123")
# q123 = """SELECT DISTINCT a11.TIME_KEY
# FROM MSADMIN.CS_AGENT_CUSTOMER_SUM a11
# --LIMIT 10
# """
# edw_join_df = spark.sql(q123)
# print(edw_join_df.count())
# edw_join_df.printSchema()
# edw_join_df.show(5)
# edw_join_df.createOrReplaceTempView("revenue1234")
query2_allows_leg_cur_ach = """select DISPLAY_SALES_CHANNEL_GROUP AS `Channel Group`,
                   SALES_CHANNEL_NM as `Channel`,
                   SALES_SUB_CHANNEL_NM as `Sub Channel`,
                   AFFILIATE_NM AS `Affiliate`,
                   EMPLOYEE_TYPE_CD as `ETC`
            from MSADMIN.CS_EMPLOYEE_TYPE_CD_XREF
            where current_flg = 'Y' 
            group by `Channel Group`, `Channel`, `Sub Channel`, `Affiliate`, `ETC`
        """

        
cs_employee_type_cd_xref_v = spark.sql(query2_allows_leg_cur_ach)
print(cs_employee_type_cd_xref_v.count())
cs_employee_type_cd_xref_v.printSchema()
cs_employee_type_cd_xref_v.show(5)
cs_employee_type_cd_xref_v.createOrReplaceTempView("cs_employee_type_cd_xref_v")
final_query = f"""
        WITH

        REVENUE AS ({query}),

        CETDCXV AS ({query2}),
        
        JOINED_NRPA AS (
            SELECT 
                REVENUE.*,
                CETDCXV.ETC AS CETDCXV_ETC,  -- Rename to avoid ambiguity
                CETDCXV.Affiliate  -- Bring Affiliate from CETDCXV
            FROM REVENUE 
            INNER JOIN CETDCXV 
            ON CETDCXV.ETC = REVENUE.EMPLOYEE_TYPE_CD
        )
        
        SELECT 
            ACCT_CHG,	
            ACCT_CHG_DISC,
            ACCT_CHG_DOWNGRADE,	
            ACCT_CHG_DOWNTIER,	
            ACCT_CHG_E_TRANSFER,	
            ACCT_CHG_NEW_CONN,	
            ACCT_CHG_NONE,	
            ACCT_CHG_OTHER,	
            ACCT_CHG_RESTART,	
            ACCT_CHG_SIDEGRADE,	
            ACCT_CHG_TRANSFER,	
            ACCT_CHG_UPGRADE,	
            ACCT_CHG_UPTIER,	
            "Affiliate",  -- Use the correct alias for Affiliate	
            CASE WHEN "Channel" IS NULL THEN "Legacy Channel" ELSE "Channel" END AS `H Channel`,	
            CASE WHEN "Channel Group" IS NULL THEN "Legacy Channel Group" ELSE "Channel Group" END AS `H Channel Group`,	
            JOINED_NRPA.CUSTOMER_SUBSTATUS_KEY AS `Customer Sub Status Key`,	
            DISPLAY_CHANNEL_GROUP_NM,
            JOINED_NRPA.CETDCXV_ETC,  -- Reference the renamed column
            CASE WHEN "ETC" IS NULL THEN "Legacy ETC" ELSE "ETC" END AS `H ETC`,	
            NRPA_DISC_NET_REV,	
            NRPA_DOWNGRADE_NET_REV,	
            NRPA_DOWNTIER_NET_REV,	
            NRPA_NET_REV,	
            NRPA_NEW_CONN_NET_REV,	
            NRPA_OTHER_NET_REV,	
            NRPA_RESTART_NET_REV,	
            NRPA_SIDEGRADE_NET_REV,	
            NRPA_TRANSFER_NET_REV,	
            NRPA_UPGRADE_NET_REV,	
            NRPA_UPTIER_NET_REV,	
            SALES_CHANNEL_NM,
            SITE_DESC AS Site,	
            SITE_KEY,	
            "Sub Channel",
            SUB_STATUS_DESC AS `Customer Sub Status`,	
            TIME_KEY AS Date
        FROM JOINED_NRPA
        INNER JOIN edw.customer_substatus_dim 
        ON edw.customer_substatus_dim.customer_substatus_key = JOINED_NRPA.CUSTOMER_SUBSTATUS_KEY
        GROUP BY 
            ACCT_CHG,
            ACCT_CHG_NONE,
            ACCT_CHG_OTHER,
            DISPLAY_CHANNEL_GROUP_NM,
            NRPA_NET_REV,
            NRPA_OTHER_NET_REV,
            SALES_CHANNEL_NM,
            SITE_KEY,
            TIME_KEY,
            SITE,
            `H Channel Group`,
            `H Channel`,
            `H ETC`,
            "Sub Channel",
            "Affiliate",  -- Group by Affiliate
            JOINED_NRPA.CUSTOMER_SUBSTATUS_KEY,
            SUB_STATUS_DESC,
            JOINED_NRPA.CETDCXV_ETC,  -- Use the renamed column here as well
            ACCT_CHG_DISC,
            ACCT_CHG_DOWNGRADE,
            ACCT_CHG_DOWNTIER,
            ACCT_CHG_NEW_CONN,
            ACCT_CHG_RESTART,
            ACCT_CHG_SIDEGRADE,
            ACCT_CHG_E_TRANSFER,
            ACCT_CHG_TRANSFER,
            ACCT_CHG_UPGRADE,
            ACCT_CHG_UPTIER,
            NRPA_DISC_NET_REV,
            NRPA_DOWNGRADE_NET_REV,
            NRPA_DOWNTIER_NET_REV,
            NRPA_NEW_CONN_NET_REV,
            NRPA_RESTART_NET_REV,
            NRPA_TRANSFER_NET_REV,
            NRPA_SIDEGRADE_NET_REV,
            NRPA_UPGRADE_NET_REV,
            NRPA_UPTIER_NET_REV
        """

        
result_df = spark.sql(final_query)
# df.createOrReplaceTempView("NRPA")
# result_df ="""select * from revenue inner join cs_employee_type_cd_xref_v where cs_employee_type_cd_xref_v.EMPLOYEE_TYPE_CD = revenue.EMPLOYEE_TYPE_CD"""
result_df.createOrReplaceTempView("result_df")
print("result")
result_df.show(5)
final_query2 = f"""
        WITH

        ACA AS ({query_aca}),

        CETDCXV AS ({query2}),
        
        JOINED_NRPA AS (
            SELECT 
                ACA.*,
                CETDCXV.ETC AS CETDCXV_ETC,  -- Rename to avoid ambiguity
                CETDCXV.Affiliate  -- Bring Affiliate from CETDCXV
            FROM ACA 
            INNER JOIN CETDCXV 
            ON CETDCXV.ETC = ACA.EMPLOYEE_TYPE_CD
        )
        
        SELECT 
            ACCT_CHG,	
            ACCT_CHG_DISC,
            ACCT_CHG_DOWNGRADE,	
            ACCT_CHG_DOWNTIER,	
            ACCT_CHG_NEW_CONN,	
            ACCT_CHG_NONE,	
            ACCT_CHG_OTHER,	
            ACCT_CHG_RESTART,	
            ACCT_CHG_SIDEGRADE,	
            ACCT_CHG_TRANSFER,	
            ACCT_CHG_UPGRADE,	
            ACCT_CHG_UPTIER,	
            "Affiliate",  -- Use the correct alias for Affiliate	
            CASE WHEN "Channel" IS NULL THEN "Legacy Channel" ELSE "Channel" END AS `H Channel`,	
            CASE WHEN "Channel Group" IS NULL THEN "Legacy Channel Group" ELSE "Channel Group" END AS `H Channel Group`,	
            JOINED_NRPA.CUSTOMER_SUBSTATUS_KEY AS `Customer Sub Status Key`,	
            DISPLAY_CHANNEL_GROUP_NM,
            JOINED_NRPA.CETDCXV_ETC,  -- Reference the renamed column
            CASE WHEN "ETC" IS NULL THEN "Legacy ETC" ELSE "ETC" END AS `H ETC`,	
            NRPA_DISC_NET_REV,	
            NRPA_DOWNGRADE_NET_REV,	
            NRPA_DOWNTIER_NET_REV,	
            NRPA_NET_REV,	
            NRPA_NEW_CONN_NET_REV,	
            NRPA_OTHER_NET_REV,	
            NRPA_RESTART_NET_REV,	
            NRPA_SIDEGRADE_NET_REV,	
            NRPA_TRANSFER_NET_REV,	
            NRPA_UPGRADE_NET_REV,	
            NRPA_UPTIER_NET_REV,	
            SALES_CHANNEL_NM,
            SITE_DESC AS Site,	
            SITE_KEY,	
            "Sub Channel",
            SUB_STATUS_DESC AS `Customer Sub Status`,	
            TIME_KEY AS Date
        FROM JOINED_NRPA
        INNER JOIN edw.customer_substatus_dim 
        ON edw.customer_substatus_dim.customer_substatus_key = JOINED_NRPA.CUSTOMER_SUBSTATUS_KEY
        GROUP BY 
            ACCT_CHG,
            ACCT_CHG_NONE,
            ACCT_CHG_OTHER,
            DISPLAY_CHANNEL_GROUP_NM,
            NRPA_NET_REV,
            NRPA_OTHER_NET_REV,
            SALES_CHANNEL_NM,
            SITE_KEY,
            TIME_KEY,
            SITE,
            `H Channel Group`,
            `H Channel`,
            `H ETC`,
            "Sub Channel",
            "Affiliate",  -- Group by Affiliate
            JOINED_NRPA.CUSTOMER_SUBSTATUS_KEY,
            SUB_STATUS_DESC,
            JOINED_NRPA.CETDCXV_ETC,  -- Use the renamed column here as well
            ACCT_CHG_DISC,
            ACCT_CHG_DOWNGRADE,
            ACCT_CHG_DOWNTIER,
            ACCT_CHG_NEW_CONN,
            ACCT_CHG_RESTART,
            ACCT_CHG_SIDEGRADE,
            ACCT_CHG_TRANSFER,
            ACCT_CHG_UPGRADE,
            ACCT_CHG_UPTIER,
            NRPA_DISC_NET_REV,
            NRPA_DOWNGRADE_NET_REV,
            NRPA_DOWNTIER_NET_REV,
            NRPA_NEW_CONN_NET_REV,
            NRPA_RESTART_NET_REV,
            NRPA_TRANSFER_NET_REV,
            NRPA_SIDEGRADE_NET_REV,
            NRPA_UPGRADE_NET_REV,
            NRPA_UPTIER_NET_REV
        """

        
result_df2 = spark.sql(final_query2)
# df.createOrReplaceTempView("NRPA")
# result_df ="""select * from revenue inner join cs_employee_type_cd_xref_v where cs_employee_type_cd_xref_v.EMPLOYEE_TYPE_CD = revenue.EMPLOYEE_TYPE_CD"""
result_df2.createOrReplaceTempView("result_df2")
print("result")
result_df2.show(5)
account_changed = """select
Date,	
Site,	
`H Channel Group`,	
`H Channel`,	
`H ETC`,	
`Sub Channel`,	
Affiliate,	
`Customer Sub Status Key`,	
`Customer Sub Status`,
ACCT_CHG_DISC AS Disconnect,
ACCT_CHG_DOWNGRADE	AS Downgrade,
ACCT_CHG_DOWNTIER	AS Downtier,
ACCT_CHG_NEW_CONN	AS `New Connect`,
ACCT_CHG_RESTART	AS Restart,
ACCT_CHG_SIDEGRADE	AS Sidegrade,	
ACCT_CHG_TRANSFER	AS Transfer,
ACCT_CHG_UPGRADE	AS Upgrade,
ACCT_CHG_UPTIER	AS Uptier from result_df"""
result_df5 = spark.sql(account_changed)
# df.createOrReplaceTempView("NRPA")
# result_df ="""select * from revenue inner join cs_employee_type_cd_xref_v where cs_employee_type_cd_xref_v.EMPLOYEE_TYPE_CD = revenue.EMPLOYEE_TYPE_CD"""
result_df5.createOrReplaceTempView("account_changed")
print("result")
result_df5.show(5)
net_revenue = """select NRPA_DISC_NET_REV AS Disconnect,
NRPA_DOWNGRADE_NET_REV AS	Downgrade,
NRPA_DOWNTIER_NET_REV AS	Downtier,
NRPA_NEW_CONN_NET_REV AS	`New Connect`,
NRPA_RESTART_NET_REV AS	Restart,
NRPA_TRANSFER_NET_REV AS	Transfer,
NRPA_SIDEGRADE_NET_REV AS	Sidegrade,
NRPA_UPGRADE_NET_REV AS	Upgrade,
NRPA_UPTIER_NET_REV AS	Uptier
from result_df"""
result_df6 = spark.sql(net_revenue)
# df.createOrReplaceTempView("NRPA")
# result_df ="""select * from revenue inner join cs_employee_type_cd_xref_v where cs_employee_type_cd_xref_v.EMPLOYEE_TYPE_CD = revenue.EMPLOYEE_TYPE_CD"""
result_df6.createOrReplaceTempView("result_df6")
print("result")
result_df6.show(5)
query7 = """select NRPA_DISC_NET_REV AS Disconnect,
NRPA_DOWNGRADE_NET_REV AS	Downgrade,
NRPA_DOWNTIER_NET_REV AS	Downtier,
NRPA_NEW_CONN_NET_REV AS	`New Connect`,
NRPA_RESTART_NET_REV AS	Restart,
NRPA_TRANSFER_NET_REV AS	Transfer,
NRPA_SIDEGRADE_NET_REV AS	Sidegrade,
NRPA_UPGRADE_NET_REV AS	Upgrade,
NRPA_UPTIER_NET_REV AS	Uptier
from result_df2"""
result_df7 = spark.sql(query7)
# df.createOrReplaceTempView("NRPA")
# result_df ="""select * from revenue inner join cs_employee_type_cd_xref_v where cs_employee_type_cd_xref_v.EMPLOYEE_TYPE_CD = revenue.EMPLOYEE_TYPE_CD"""
result_df7.createOrReplaceTempView("result_df7")
print("result")
result_df7.show(5)
job.commit()