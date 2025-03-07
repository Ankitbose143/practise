from pyspark.sql import SparkSession, DataFrame

class DNRV1:

    def initial_process_data():
        try:

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
            
            query2_allows_leg_cur_ach = """select DISPLAY_SALES_CHANNEL_GROUP AS `Channel Group`,
                       SALES_CHANNEL_NM as `Channel`,
                       SALES_SUB_CHANNEL_NM as `Sub Channel`,
                       AFFILIATE_NM AS `Affiliate`,
                       EMPLOYEE_TYPE_CD as `ETC`
                from MSADMIN.CS_EMPLOYEE_TYPE_CD_XREF
                where current_flg = 'Y' 
                group by `Channel Group`, `Channel`, `Sub Channel`, `Affiliate`, `ETC`
            """

            
            final_query = f"""
            WITH

            REVENUE AS ({query_revenue}),

            CETDCXV AS ({query2_allows_leg_cur_ach}),
            
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
                DISPLAY_CHANNEL_GROUP_NM AS `H Channel Group`,
                SALES_CHANNEL_NM AS `H Channel`,
                "Affiliate",  -- Use the correct alias for Affiliate	            
                CASE WHEN "Channel" IS NULL THEN SALES_CHANNEL_NM ELSE "Channel" END AS `Channel`,	            
                CASE WHEN "Channel Group" IS NULL THEN DISPLAY_CHANNEL_GROUP_NM ELSE "Channel Group" END AS `Channel Group`,	
                JOINED_NRPA.CUSTOMER_SUBSTATUS_KEY AS `Customer Sub Status Key`,	            
                JOINED_NRPA.CETDCXV_ETC,  -- Reference the renamed column
                EMPLOYEE_TYPE_CD AS `H ETC`,
                CASE WHEN "ETC" IS NULL THEN EMPLOYEE_TYPE_CD ELSE "ETC" END AS `ETC`,	
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
                ETC,
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

            
            
            #df = spark.sql(final_query)
            #df.createOrReplaceTempView("NRPA")
            #return df
            
            final_query2 = f"""
            WITH

            ACA AS ({query_aca}),

            CETDCXV AS ({query2_allows_leg_cur_ach}),
            
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
                DISPLAY_CHANNEL_GROUP_NM AS `H Channel Group`,
                SALES_CHANNEL_NM AS `H Channel`,
                "Affiliate",  -- Use the correct alias for Affiliate	            
                CASE WHEN "Channel" IS NULL THEN SALES_CHANNEL_NM ELSE "Channel" END AS `Channel`,	            
                CASE WHEN "Channel Group" IS NULL THEN DISPLAY_CHANNEL_GROUP_NM ELSE "Channel Group" END AS `Channel Group`,	
                JOINED_NRPA.CUSTOMER_SUBSTATUS_KEY AS `Customer Sub Status Key`,	            
                JOINED_NRPA.CETDCXV_ETC,  -- Reference the renamed column
                EMPLOYEE_TYPE_CD AS `H ETC`,
                CASE WHEN "ETC" IS NULL THEN EMPLOYEE_TYPE_CD ELSE "ETC" END AS `ETC`,	
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
                ETC,
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
            return final_query
        except Exception as err:
            print("Error: initial_process_data", err)

    def initial_process_data2():
        try:

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
            
            query2_allows_leg_cur_ach = """select DISPLAY_SALES_CHANNEL_GROUP AS `Channel Group`,
                       SALES_CHANNEL_NM as `Channel`,
                       SALES_SUB_CHANNEL_NM as `Sub Channel`,
                       AFFILIATE_NM AS `Affiliate`,
                       EMPLOYEE_TYPE_CD as `ETC`
                from MSADMIN.CS_EMPLOYEE_TYPE_CD_XREF
                where current_flg = 'Y' 
                group by `Channel Group`, `Channel`, `Sub Channel`, `Affiliate`, `ETC`
            """

            
            
            
            final_query2 = f"""
            WITH

            ACA AS ({query_aca}),

            CETDCXV AS ({query2_allows_leg_cur_ach}),
            
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
                DISPLAY_CHANNEL_GROUP_NM AS `H Channel Group`,
                SALES_CHANNEL_NM AS `H Channel`,
                "Affiliate",  -- Use the correct alias for Affiliate	            
                CASE WHEN "Channel" IS NULL THEN SALES_CHANNEL_NM ELSE "Channel" END AS `Channel`,	            
                CASE WHEN "Channel Group" IS NULL THEN DISPLAY_CHANNEL_GROUP_NM ELSE "Channel Group" END AS `Channel Group`,	
                JOINED_NRPA.CUSTOMER_SUBSTATUS_KEY AS `Customer Sub Status Key`,	            
                JOINED_NRPA.CETDCXV_ETC,  -- Reference the renamed column
                EMPLOYEE_TYPE_CD AS `H ETC`,
                CASE WHEN "ETC" IS NULL THEN EMPLOYEE_TYPE_CD ELSE "ETC" END AS `ETC`,	
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
                ETC,
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
            return final_query2
        except Exception as err:
            print("Error: initial_process_data2", err)
   
    @staticmethod
    def account_changed(result_df):
        try:
            #result_df.createOrReplaceTempView(result_df)
            account_changed = f"""select
                        Date,	
                        Site,	
                        `H Channel Group`,	
                        `H Channel`,	
                        `H ETC`,	
                        `Channel Group`,
                        `Channel`,
                        ETC,
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
                        ACCT_CHG_UPTIER	AS Uptier from {result_df}"""
            return  account_changed 
        except Exception as err:
            print("Error: account_changed", err)
            
            
    def net_revenue(result_df):
        try:
            net_revenue = f"""select 
                        Date,	
                        Site,	
                        `H Channel Group`,	
                        `H Channel`,	
                        `H ETC`,	
                        `Channel Group`,
                        `Channel`,
                        ETC,
                        `Sub Channel`,	
                        Affiliate,	
                        `Customer Sub Status Key`,	
                        `Customer Sub Status`,
                        NRPA_DISC_NET_REV AS Disconnect,
                        NRPA_DOWNGRADE_NET_REV AS	Downgrade,
                        NRPA_DOWNTIER_NET_REV AS	Downtier,
                        NRPA_NEW_CONN_NET_REV AS	`New Connect`,
                        NRPA_RESTART_NET_REV AS	Restart,
                        NRPA_TRANSFER_NET_REV AS	Transfer,
                        NRPA_SIDEGRADE_NET_REV AS	Sidegrade,
                        NRPA_UPGRADE_NET_REV AS	Upgrade,
                        NRPA_UPTIER_NET_REV AS	Uptier
                        from {result_df}"""
            return  net_revenue
        except Exception as err:
            print("Error: net_revenue", err)
            
    
    def account_changed_all(result_df):
        try:
            account_changed_all = f"""select
                        Date,	
                        Site,	
                        `H Channel Group`,	
                        `H Channel`,	
                        `H ETC`,	
                        `Channel Group`,
                        `Channel`,
                        ETC,
                        `Sub Channel`,	
                        Affiliate,	
                        `Customer Sub Status Key`,	
                        `Customer Sub Status`,
                        NRPA_DISC_NET_REV AS Disconnect,
                        NRPA_DOWNGRADE_NET_REV AS	Downgrade,
                        NRPA_DOWNTIER_NET_REV AS	Downtier,
                        NRPA_NEW_CONN_NET_REV AS	`New Connect`,
                        NRPA_RESTART_NET_REV AS	Restart,
                        NRPA_TRANSFER_NET_REV AS	Transfer,
                        NRPA_SIDEGRADE_NET_REV AS	Sidegrade,
                        NRPA_UPGRADE_NET_REV AS	Upgrade,
                        NRPA_UPTIER_NET_REV AS	Uptier
                        from {result_df}"""
            return  account_changed_all 
        except Exception as err:
            print("Error: account_changed_all", err)
            

    def ac_nr(result_df6):
        try:
            df_ac_nr = f"""
                SELECT 
                    Date,
                    Site,
                    `H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    `Channel Group`,
                    `Channel`,
                    ETC,
                    `Sub Channel`,
                    Affiliate,
                    `Customer Sub Status Key`,
                    `Customer Sub Status`,
                    activity,
                    SUM(`Accounts Changed All`) AS `Accounts Changed All`,
                    SUM(`Accounts Changed`) AS `Accounts Changed`,
                    SUM(`Net Revenue`) AS `Net Revenue`
                FROM (
                    -- For Accounts Changed All
                    SELECT 
                        Date,
                        Site,
                        `H Channel Group`,
                        `H Channel`,
                        `H ETC`,
                        `Channel Group`,
                        `Channel`,
                        ETC,
                        `Sub Channel`,
                        Affiliate,
                        `Customer Sub Status Key`,
                        `Customer Sub Status`,
                        stack(9, 
                              'Disconnect', Disconnect, 
                              'Downgrade', Downgrade, 
                              'Downtier', Downtier, 
                              'New Connect', `New Connect`, 
                              'Restart', Restart, 
                              'Transfer', Transfer, 
                              'Sidegrade', Sidegrade, 
                              'Upgrade', Upgrade, 
                              'Uptier', Uptier) 
                        AS (activity, `Accounts Changed All`),
                        NULL AS `Accounts Changed`,
                        NULL AS `Net Revenue`
                    FROM {result_df6}

                    UNION ALL

                    -- For Accounts Changed
                    SELECT 
                        Date,
                        Site,
                        `H Channel Group`,
                        `H Channel`,
                        `H ETC`,
                        `Channel Group`,
                        `Channel`,
                        ETC,
                        `Sub Channel`,
                        Affiliate,
                        `Customer Sub Status Key`,
                        `Customer Sub Status`,
                        stack(9, 
                              'Disconnect', Disconnect, 
                              'Downgrade', Downgrade, 
                              'Downtier', Downtier, 
                              'New Connect', `New Connect`, 
                              'Restart', Restart, 
                              'Transfer', Transfer, 
                              'Sidegrade', Sidegrade, 
                              'Upgrade', Upgrade, 
                              'Uptier', Uptier) 
                        AS (activity, `Accounts Changed`),
                        NULL AS `Accounts Changed All`,
                        NULL AS `Net Revenue`
                    FROM {result_df6}

                    UNION ALL

                    -- For Net Revenue
                    SELECT 
                        Date,
                        Site,
                        `H Channel Group`,
                        `H Channel`,
                        `H ETC`,
                        `Channel Group`,
                        `Channel`,
                        ETC,
                        `Sub Channel`,
                        Affiliate,
                        `Customer Sub Status Key`,
                        `Customer Sub Status`,
                        stack(9, 
                              'Disconnect', Disconnect, 
                              'Downgrade', Downgrade, 
                              'Downtier', Downtier, 
                              'New Connect', `New Connect`, 
                              'Restart', Restart, 
                              'Transfer', Transfer, 
                              'Sidegrade', Sidegrade, 
                              'Upgrade', Upgrade, 
                              'Uptier', Uptier) 
                        AS (activity, `Net Revenue`),
                        NULL AS `Accounts Changed All`,
                        NULL AS `Accounts Changed`
                    FROM {result_df6}
                ) AS combined_table
                WHERE 
                    `Accounts Changed All` IS NOT NULL 
                    OR `Accounts Changed` IS NOT NULL 
                    OR `Net Revenue` IS NOT NULL
                GROUP BY 
                    Date,
                    Site,
                    `H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    `Channel Group`,
                    `Channel`,
                    ETC,
                    `Sub Channel`,
                    Affiliate,
                    `Customer Sub Status Key`,
                    `Customer Sub Status`,
                    activity
                HAVING SUM(`Accounts Changed All`) <> 0 
                   OR SUM(`Accounts Changed`) <> 0 
                   OR SUM(`Net Revenue`) <> 0;
                """
            return df_ac_nr
        except Exception as err:
            print("Error: ac_nr", err)
            #df_ac_nr.show(5)
            #df_ac_nr.createOrReplaceTempView("df_ac_nr")
            

    
            
            
    def df_ac_nr_maxdatesql(result_df7):
        try:
            df_ac_nr_maxdatesql = f"""
                WITH metrics AS (
                SELECT 
                    Date,
                    Site,
                    `H Channel Group`,
                    CASE 
                        WHEN `H Channel` = 'Cox Owned Retail' THEN 'Retail'
                        WHEN `H Channel` = 'Cox Owned - Retail' THEN 'Retail'
                        ELSE `H Channel`
                    END AS `H Channel`,
                    `H ETC`,
                    CASE 
                        WHEN `Channel Group` = 'Cox Owned Retail' THEN 'Retail'
                        WHEN `Channel Group` = 'Cox Owned - Retail' THEN 'Retail'
                        when `Channel Group` = 'Web Sales' THEN 'Online'
                        ELSE `Channel Group`
                    END AS `Channel Group`,
                    CASE 
                        WHEN `Sub Channel` = '3rd Party - Affinity' 
                             OR `Sub Channel` = 'Online - Referral' THEN 'National Affiliates'
                         WHEN `Sub Channel` LIKE '%Online -%' 
                             OR `Sub Channel` LIKE '%web%' 
                             OR `Sub Channel` LIKE '%Third Party Online%'
                             OR `Sub Channel` LIKE '%Sub Channel%' THEN 'Cox.com'
                        
                        --WHEN CONTAINS(`Sub Channel`, 'Online -', 'web','Third Party Online') THEN 'Cox.com'
                        WHEN `Sub Channel` = '3rd Party - eTailer' THEN 'eTailers'
                        WHEN `Channel` = 'eTail' THEN 'eTailers'
                        WHEN IsNull(`Channel`) THEN `Channel Group`
                        ELSE `Channel`
                    END AS `Channel`,
                    ETC,
                    `Sub Channel`,
                    Affiliate,
                    `Customer Sub Status Key`,
                    `Customer Sub Status`,
                    activity,
                    SUM(`Accounts Changed All`) AS `Accounts Changed All`,
                    SUM(`Accounts Changed`) AS `Accounts Changed`,
                    SUM(`Net Revenue`) AS `Net Revenue`
                FROM (
                    -- For Accounts Changed All
                    SELECT 
                        Date,
                        Site,
                        `H Channel Group`,
                        `H Channel`,
                        `H ETC`,
                        `Channel Group`,
                        `Channel`,
                        ETC,
                        `Sub Channel`,
                        Affiliate,
                        `Customer Sub Status Key`,
                        `Customer Sub Status`,
                        stack(9, 
                              'Disconnect', Disconnect, 
                              'Downgrade', Downgrade, 
                              'Downtier', Downtier, 
                              'New Connect', `New Connect`, 
                              'Restart', Restart, 
                              'Transfer', Transfer, 
                              'Sidegrade', Sidegrade, 
                              'Upgrade', Upgrade, 
                              'Uptier', Uptier) 
                        AS (activity, `Accounts Changed All`),
                        NULL AS `Accounts Changed`,
                        NULL AS `Net Revenue`
                    FROM {result_df7}

                    UNION ALL

                    -- For Accounts Changed
                    SELECT 
                        Date,
                        Site,
                        `H Channel Group`,
                        `H Channel`,
                        `H ETC`,
                        `Channel Group`,
                        `Channel`,
                        ETC,
                        `Sub Channel`,
                        Affiliate,
                        `Customer Sub Status Key`,
                        `Customer Sub Status`,
                        stack(9, 
                              'Disconnect', Disconnect, 
                              'Downgrade', Downgrade, 
                              'Downtier', Downtier, 
                              'New Connect', `New Connect`, 
                              'Restart', Restart, 
                              'Transfer', Transfer, 
                              'Sidegrade', Sidegrade, 
                              'Upgrade', Upgrade, 
                              'Uptier', Uptier) 
                        AS (activity, `Accounts Changed`),
                        NULL AS `Accounts Changed All`,
                        NULL AS `Net Revenue`
                    FROM {result_df7}

                    UNION ALL

                    -- For Net Revenue
                    SELECT 
                        Date,
                        Site,
                        `H Channel Group`,
                        `H Channel`,
                        `H ETC`,
                        `Channel Group`,
                        `Channel`,
                        ETC,
                        `Sub Channel`,
                        Affiliate,
                        `Customer Sub Status Key`,
                        `Customer Sub Status`,
                        stack(9, 
                              'Disconnect', Disconnect, 
                              'Downgrade', Downgrade, 
                              'Downtier', Downtier, 
                              'New Connect', `New Connect`, 
                              'Restart', Restart, 
                              'Transfer', Transfer, 
                              'Sidegrade', Sidegrade, 
                              'Upgrade', Upgrade, 
                              'Uptier', Uptier) 
                        AS (activity, `Net Revenue`),
                        NULL AS `Accounts Changed All`,
                        NULL AS `Accounts Changed`
                    FROM {result_df7}
                ) AS combined_table
                WHERE 
                    `Accounts Changed All` IS NOT NULL 
                    OR `Accounts Changed` IS NOT NULL 
                    OR `Net Revenue` IS NOT NULL
                GROUP BY 
                    Date,
                    Site,
                    `H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    `Channel Group`,
                    `Channel`,
                    ETC,
                    `Sub Channel`,
                    Affiliate,
                    `Customer Sub Status Key`,
                    `Customer Sub Status`,
                    activity
                HAVING SUM(`Accounts Changed All`) <> 0 
                   OR SUM(`Accounts Changed`) <> 0 
                   OR SUM(`Net Revenue`) <> 0
            ),

            max_date AS (
                SELECT 
                    MAX(Date) AS Max_Date
                FROM metrics
            )

            SELECT 
                m.Date,
                --CASE
                    --WHEN m.`Channel` = 'DIRECT SALES REP - SFU' THEN 'Door to Door Sales'
                    --WHEN m.`Channel` = 'DIRECT SALES REP - MDU' THEN 'Door to Door Sales'
                    --WHEN m.`Channel` = 'Door to Door Save Team' THEN 'Home Security Inbound'
                    --WHEN m.`Sub Channel` = '3rd Party - Affinity' OR m.`Sub Channel` = 'Online - Referral' THEN 'National Affiliates'
                    --WHEN m.`Sub Channel` LIKE '%Online -%' THEN 'Cox.com'
                    --WHEN m.`Sub Channel` = '3rd Party - eTailer' THEN 'eTailers'
                    --WHEN m.`Channel` = 'eTail' THEN 'eTailers'
                    --WHEN IsNull(m.`Channel`) THEN `Channel Group`
                    --ELSE m.`Channel`
                --END AS `Channel`,
                --CASE
                    --WHEN m.`Channel` = 'Cox Owned Leadership' THEN 'Retail'
                    --WHEN m.`Channel` = 'Digital Store' THEN 'Retail'
                    --WHEN m.`Channel` = 'Kiosk' THEN 'Retail'
                    --WHEN m.`Channel` = '3rd Party - Exclusive Dealer' THEN 'Retail'        
                    --WHEN m.`Channel` = 'Direct Sales Outsourced' THEN 'Field Sales'
                    --WHEN m.`Channel` = 'Direct Sales Leadership' THEN 'Field Sales'
                    --WHEN m.`Channel` = 'Door to Door Sales' THEN 'Field Sales'
                    --WHEN m.`Channel` = 'Field Sales Leadership' THEN 'Field Sales'
                    --WHEN m.`Channel` = 'Home Security Direct Sales' THEN 'Field Sales'
                    --WHEN m.`Channel` = '3rd Party - Authorized Dealer' THEN 'Field Sales'
                    --WHEN m.`Channel` = '3rd Party - Big Box' THEN 'Field Sales'
                    --WHEN m.`Channel` = '3rd Party - Boost Mobile' THEN 'Field Sales'
                    --WHEN m.`Channel` = '3rd Party - Military' THEN 'Field Sales'
                    --WHEN m.`Channel` = '3rd Party - Military Exchange' THEN 'Field Sales'
                    --WHEN m.`Channel` = '3rd Party - Mobility' THEN 'Field Sales'
                    --WHEN m.`Channel` = '3rd Party Leadership Support' THEN 'Field Sales'
                    --WHEN m.`Channel` = 'DIRECT SALES REP - SFU' THEN 'Field Sales'
                    --WHEN m.`Channel` = 'DIRECT SALES REP - MDU' THEN 'Field Sales'        
                    --WHEN m.`Channel` = 'Door to Door Save Team' THEN 'Home Security'        
                    --WHEN m.`Channel` = 'MDU AE' THEN 'Lead Referral'     
                    ---WHEN m.`Channel Group` ='Lead Referral' THEN 'Other'
                    --ELSE m.`Channel Group`
                --END AS `Channel Group`,
                m.`Channel`,
                m.`Channel Group`,
                m.`Activity`,
                --CASE
                    --WHEN m.`Channel` = 'DIRECT SALES REP - SFU' THEN 'DIRECT SALES REP - SFU'
                    --WHEN m.`Channel` = 'DIRECT SALES REP - MDU' THEN 'DIRECT SALES REP - MDU'
                    --ELSE m.`Sub Channel`
                --END AS `Sub Channel`,
                m.`Sub Channel`,
                m.Site,
                --CASE 
                    --WHEN m.`H Channel Group` = 'Lead Referral' THEN 'Other'
                    --ELSE m.`H Channel Group` 
                --END AS `H Channel Group`,
                --CASE 
                    --WHEN m.`H Channel Group` IN ('Online', 'Inbound', 'Retail', 'Field Sales', 'Retention', 'Care') THEN m.`H Channel Group`
                    --ELSE 'Other'
                --END AS `H Channel`,
                m.`H Channel Group`,
                m.`H Channel`,
                m.`H ETC`,
                m.Affiliate,
                m.ETC,
                m.`Customer Sub Status Key`,
                m.`Customer Sub Status`,
                --SUM(m.`Accounts Changed`) AS `Accounts Changed`,
                --SUM(m.`Net Revenue`) AS `Net Revenue`,
                --SUM(m.`Accounts Changed All`) AS `Accounts Changed All`,
                m.`Accounts Changed`,
                m.`Accounts Changed All`,
                m.`Net Revenue`,
                md.Max_Date
            FROM metrics m
            JOIN max_date md
            ON m.Date = md.Max_Date
            --WHERE md.Max_Date <> DATEADD(day, -1, CURRENT_DATE())
            --AND (m.`Channel Group` NOT IN ('Call Center Flex', 'Home Security'))
            --AND m.`Activity` NOT IN ('Sidegrade')
                
                """
            return df_ac_nr_maxdatesql
        except Exception as err:
            print("Error: df_ac_nr_maxdatesql", err)
            #df_ac_nr.show(5)
            #df_ac_nr.createOrReplaceTempView("df_ac_nr")
            
    def df_ac_nr_maxdatesql_rename(df_ac_nr_maxdatesql):
        try:
            df_ac_nr_maxdatesql_rename = f"""
                    SELECT
                    Date,
                    CASE
                        WHEN Channel = 'Web' THEN 'Cox.com'
                        WHEN Channel = 'Third Party Online' THEN 'Cox.com'
                        ELSE Channel
                    END AS Channel,
                    CASE
                        WHEN `Channel Group` = 'Cox Owned Retail' THEN 'Retail'
                        WHEN `Channel Group` = 'Cox Owned - Retail' THEN 'Retail'
                        WHEN `Channel Group` = 'Web Sales' THEN 'Online'
                        ELSE `Channel Group`
                    END AS `Channel Group`,
                    Activity,
                    `Sub Channel`,
                    Site,
                    CASE
                        WHEN `H Channel Group` = 'Cox Owned Retail' THEN 'Retail'
                        WHEN `H Channel Group` = 'Cox Owned - Retail' THEN 'Retail'
                        ELSE `H Channel Group`
                    END AS `H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    Affiliate,
                    ETC,
                    `Customer Sub Status Key`,
                    `Customer Sub Status`,
                    `Accounts Changed`,
                    `Accounts Changed All`,
                    `Net Revenue`,
                    Max_Date
                FROM
                    {df_ac_nr_maxdatesql}
                """
            return df_ac_nr_maxdatesql_rename
        except Exception as err:
            print("Error: df_ac_nr_maxdatesql_rename", err)
            #df_ac_nr.show(5)
            #df_ac_nr.createOrReplaceTempView("df_ac_nr")
            
    def df_ac_nr_maxdatesql_dmas(df_ac_nr_maxdatesql_rename):
        try:
            df_ac_nr_maxdatesql_dmas = f"""
                     SELECT 
                    Date,
                    CASE 
                        WHEN `Sub Channel` = '3rd Party - Affinity' OR `Sub Channel` = 'Online - Referral' THEN 'National Affiliates'
                        WHEN `Sub Channel` LIKE 'Online -%' THEN 'Cox.com'
                        WHEN `Sub Channel` = '3rd Party - eTailer' THEN 'eTailers'
                        WHEN Channel = 'eTail' THEN 'eTailers'
                        WHEN Channel IS NULL THEN `Channel Group`
                        ELSE Channel
                    END AS Channel,
                    `Channel Group`,
                    Activity,
                    `Sub Channel`,
                    Site,
                    `H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    Affiliate,
                    ETC,
                    `Customer Sub Status Key`,
                    `Customer Sub Status`,
                    `Accounts Changed`,
                    `Accounts Changed All`,
                    `Net Revenue`,
                    Max_Date
                FROM {df_ac_nr_maxdatesql_rename}
                """
            return df_ac_nr_maxdatesql_dmas
        except Exception as err:
            print("Error: df_ac_nr_maxdatesql_dmas", err)
            

    def df_ac_nr_maxdatesql_mcr(df_ac_nr_maxdatesql_dmas):
        try:
            df_ac_nr_maxdatesql_mcr = f"""
                    SELECT 
                    Date,
                    CASE
                        WHEN Channel = 'Web' THEN 'Cox.com'
                        WHEN Channel = 'Third Party Online' THEN 'Cox.com'
                        ELSE Channel
                    END AS Channel,
                    CASE
                        WHEN `Channel Group` = 'Cox Owned Retail' THEN 'Retail'
                        WHEN `Channel Group` = 'Cox Owned - Retail' THEN 'Retail'
                        WHEN `Channel Group` = 'Web Sales' THEN 'Online'
                        ELSE `Channel Group`
                    END AS `Channel Group`,
                    --`Channel Group`,
                    Activity,
                    `Sub Channel`,
                    Site,
                    CASE
                        WHEN `H Channel Group` = 'Cox Owned Retail' THEN 'Retail'
                        WHEN `H Channel Group` = 'Cox Owned - Retail' THEN 'Retail'
                        ELSE `H Channel Group`
                    END AS `H Channel Group`,
                    --`H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    Affiliate,
                    ETC,
                    `Customer Sub Status Key`,
                    `Customer Sub Status`,
                    `Accounts Changed`,
                    `Accounts Changed All`,
                    `Net Revenue`,
                    Max_Date
                FROM {df_ac_nr_maxdatesql_dmas}
                """
            return df_ac_nr_maxdatesql_mcr
        except Exception as err:
            print("Error: df_ac_nr_maxdatesql_mcr", err)
            
            
    def df_ac_nr_maxdatesql_rr(df_ac_nr_maxdatesql_mcr):
        try:
            df_ac_nr_maxdatesql_rr = f"""
                    SELECT 
                    Date,
                    CASE
                        WHEN Channel IN ('DIRECT SALES REP - SFU','DIRECT SALES REP - MDU') THEN 'Door to Door Sales'
                        WHEN Channel = 'Door to Door Save Team' THEN 'Home Security Inbound'
                        ELSE Channel            
                    END AS Channel,
                    CASE
                        WHEN Channel = 'Cox Owned Leadership' THEN 'Retail'
                        WHEN Channel = 'Digital Store' THEN 'Retail'
                        WHEN Channel = 'Kiosk' THEN 'Retail'
                        WHEN Channel = '3rd Party - Exclusive Dealer' THEN 'Retail'
                        WHEN Channel = 'Direct Sales Outsourced' THEN 'Field Sales'
                        WHEN Channel = 'Direct Sales Leadership' THEN 'Field Sales'
                        WHEN Channel = 'Door to Door Sales' THEN 'Field Sales'
                        WHEN Channel = 'Field Sales Leadership' THEN 'Field Sales'
                        WHEN Channel = 'Home Security Direct Sales' THEN 'Field Sales'
                        WHEN Channel = '3rd Party - Authorized Dealer' THEN 'Field Sales'
                        WHEN Channel = '3rd Party - Big Box' THEN 'Field Sales'
                        WHEN Channel = '3rd Party - Boost Mobile' THEN 'Field Sales'
                        WHEN Channel = '3rd Party - Military' THEN 'Field Sales'
                        WHEN Channel = '3rd Party - Military Exchange' THEN 'Field Sales'
                        WHEN Channel = '3rd Party - Mobility' THEN 'Field Sales'
                        WHEN Channel = '3rd Party Leadership Support' THEN 'Field Sales'
                        WHEN Channel = 'DIRECT SALES REP - SFU' THEN 'Field Sales'
                        WHEN Channel = 'DIRECT SALES REP - MDU' THEN 'Field Sales'
                        WHEN Channel = 'Door to Door Save Team' THEN 'Home Security'
                        WHEN Channel = 'MDU AE' THEN 'Lead Referral'
                        WHEN `Channel Group` = 'Lead Referral' THEN 'Other'
                        WHEN `Channel Group` IN ('Online','Inbound','Retail','Field Sales','Retention','Care') THEN `Channel Group`
                        --ELSE 'Other'
                        
                        ELSE `Channel Group`
                    END AS `Channel Group`,
                    Activity,
                    CASE
                        WHEN Channel = 'DIRECT SALES REP - SFU' THEN 'DIRECT SALES REP - SFU'
                        WHEN Channel = 'DIRECT SALES REP - MDU' THEN 'DIRECT SALES REP - MDU'
                        ELSE `Sub Channel`
                    END AS `Sub Channel`,
                    Site,
                    CASE
                        WHEN `H Channel Group` = 'Lead Referral' THEN 'Other'
                        WHEN `H Channel Group` IN ('Online','Inbound','Retail','Field Sales','Retention','Care') THEN `H Channel Group`
                        ELSE `H Channel Group`
                    END AS `H Channel Group`,        
                    `H Channel`,
                    `H ETC`,
                    Affiliate,
                    ETC,
                    `Customer Sub Status Key`,
                    `Customer Sub Status`,
                    `Accounts Changed`,
                    `Accounts Changed All`,
                    `Net Revenue`,
                    Max_Date
                FROM {df_ac_nr_maxdatesql_mcr}
                """
            return df_ac_nr_maxdatesql_rr
        except Exception as err:
            print("Error: df_ac_nr_maxdatesql_rr", err)
            

    def df_ac_nr_maxdatesql_filter_tf(df_ac_nr_maxdatesql_rr):
        try:
            df_ac_nr_maxdatesql_filter_tf = f"""
                    SELECT 
                    Date,
                    `Channel Group`,
                    CASE
                        WHEN `Channel Group` = 'Online' THEN Channel
                        ELSE `Channel Group`
                    END AS Channel, 
                    Activity,
                    CASE
                        WHEN Activity IN ('New Connect', 'Restart') THEN 'New Connect'
                        WHEN Activity IN ('Uptier', 'Upgrade') THEN '+ Base'
                        WHEN Activity IN ('Downtier', 'Downgrade') THEN '- Base'
                        WHEN Activity = 'Transfer' THEN 'Transfer'
                        WHEN Activity = 'Disconnect' THEN 'Disconnect'
                        ELSE Activity
                    END AS `Activity Base`,
                    --Activity,
                    `Sub Channel`,
                    Site,
                    `H Channel Group`,        
                    `H Channel`,
                    `H ETC`,
                    Affiliate,
                    ETC,
                    `Customer Sub Status Key`,
                    `Customer Sub Status`,
                    `Accounts Changed`,
                    `Accounts Changed All`,
                    `Net Revenue`,
                    Max_Date        
                FROM {df_ac_nr_maxdatesql_rr}
                WHERE (`Channel Group` NOT IN ('Call Center Flex', 'Home Security'))
                   AND `Activity` NOT IN ('Sidegrade')
                """
            return df_ac_nr_maxdatesql_filter_tf
        except Exception as err:
            print("Error: df_ac_nr_maxdatesql_filter_tf", err)


    def df_ac_nr_maxdatesql_group(df_ac_nr_maxdatesql):
        try:
            df_ac_nr_maxdatesql_group = f"""
                WITH aggregated_data AS (
                SELECT
                    Date,
                    `Channel Group`,
                    `Channel`,
                    `Activity`,
                    `Sub Channel`,
                    Site,
                    `H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    Affiliate,
                    ETC,
                    `Customer Sub Status`,
                    SUM(`Accounts Changed`) AS `Accounts Changed`,
                    SUM(`Net Revenue`) AS `Net Revenue`,
                    SUM(`Accounts Changed All`) AS `Accounts Changed All`
                FROM {df_ac_nr_maxdatesql}
                GROUP BY
                    Date,
                    `Channel Group`,
                    `Channel`,
                    `Activity`,
                    `Sub Channel`,
                    Site,
                    `H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    Affiliate,
                    ETC,
                    `Customer Sub Status`
            )

            SELECT *
            FROM aggregated_data
                """
            return df_ac_nr_maxdatesql_group
        except Exception as err:
            print("Error: df_ac_nr_maxdatesql_group", err)
            

    def df_data_gen():
        try:
            df_data_gen = f"""
                WITH Date_Sequence AS(
                    SELECT 
                    EXPLODE(SEQUENCE(TO_DATE('2017-01-01'), CURRENT_DATE - INTERVAL 1 DAY, INTERVAL 1 DAY)) AS `Date`
                ),
                Channels AS (
                    SELECT 'Online' AS `Channel Group`, 'eTailers' AS `Channel` UNION ALL
                    SELECT 'Online' AS `Channel Group`, 'National Affiliates' AS `Channel` UNION ALL
                    SELECT 'Online' AS `Channel Group`, 'Cox.com' AS `Channel` UNION ALL
                    SELECT 'Inbound' AS `Channel Group`, 'Inbound' AS `Channel` UNION ALL
                    SELECT 'Retail' AS `Channel Group`, 'Retail' AS `Channel` UNION ALL
                    SELECT 'Care' AS `Channel Group`, 'Care' AS `Channel` UNION ALL
                    SELECT 'Field Sales' AS `Channel Group`, 'Field Sales' AS `Channel` UNION ALL
                    SELECT 'Retention' AS `Channel Group`, 'Retention' AS `Channel` UNION ALL
                    SELECT 'Other' AS `Channel Group`, 'Other' AS `Channel`
                ),
                Activities AS (
                    SELECT 'Disconnect' AS `Activity` UNION ALL
                    SELECT 'Downgrade' AS `Activity` UNION ALL
                    SELECT 'Downtier' AS `Activity` UNION ALL
                    SELECT 'Transfer' AS `Activity` UNION ALL
                    SELECT 'Upgrade' AS `Activity` UNION ALL
                    SELECT 'New Connect' AS `Activity` UNION ALL
                    SELECT 'Uptier' AS `Activity` UNION ALL
                    SELECT 'Restart' AS `Activity`
                )
                SELECT
                    ds.`Date`,
                    c.`Channel Group`,
                    c.`Channel`,
                    a.`Activity`
                FROM
                    Date_Sequence ds
                CROSS JOIN
                    Channels c
                CROSS JOIN
                    Activities a
                """
            return df_data_gen
        except Exception as err:
            print("Error: df_data_gen", err)

    def df_ac_nr_maxdatesql_final_query(df_ac_nr_maxdatesql_filter_tf):
        try:
            df_ac_nr_maxdatesql_final_query = f"""
                    SELECT 
                    Date,
                    `Channel Group`,
                    Channel,
                    Activity,
                    `Sub Channel`,
                    Site,
                    `H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    Affiliate,
                    ETC,
                    `Customer Sub Status`,
                    SUM(`Accounts Changed`) AS `Accounts Changed`,
                    SUM(`Net Revenue`) AS `Net Revenue`,
                    `Accounts Changed All`,
                    `Activity Base`
                FROM 
                    {df_ac_nr_maxdatesql_filter_tf}
                GROUP BY 
                    Date,
                    `Channel Group`,
                    Channel,
                    Activity,
                    `Sub Channel`,
                    Site,
                    `H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    Affiliate,
                    ETC,
                    `Customer Sub Status`,
                    `Accounts Changed All`,
                    `Activity Base`
                """
            return df_ac_nr_maxdatesql_final_query
        except Exception as err:
            print("Error: df_ac_nr_maxdatesql_final_query", err)
            
            
    def query_right(df_ac_nr_maxdatesql_final_query,df_data_gen):
        try:
            query_right = f"""
                    SELECT 
                    f.*,
                    --0 as `Accounts Changed`,
                    d.`Date` AS Right_Date,
                    d.`Channel` AS Right_Channel,
                    d.`Channel Group` AS `Right_Channel Group`,
                    d.`Activity` AS Right_Activity
                FROM 
                    df_ac_nr_maxdatesql_final_query f
                RIGHT JOIN 
                    df_data_gen d
                ON 
                    f.`Date` = d.`Date` AND 
                    f.`Channel Group` = d.`Channel Group` AND 
                    f.`Channel` = d.`Channel` AND 
                    f.`Activity` = d.`Activity` 
                """
            return query_right
        except Exception as err:
            print("Error: query_right", err)
            
    def union_df(df_ac_nr_maxdatesql_final_query,query_right):
        try:
            union_df = f"""
                    SELECT 
                    Date,
                    `Channel Group`,
                    Channel,
                    Activity,
                    `Sub Channel`,
                    Site,
                    `H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    Affiliate,
                    ETC,
                    `Customer Sub Status`,
                    `Accounts Changed`,
                    `Net Revenue`,
                    `Accounts Changed All`,
                    `Activity Base`
                FROM 
                    {df_ac_nr_maxdatesql_final_query}

                UNION ALL

                SELECT 
                    Right_Date,
                    `Right_Channel Group`,
                    Right_Channel,
                    Right_Activity,
                    --Date,
                    --`Channel Group`,
                    --Channel,
                    --Activity,
                    `Sub Channel`,
                    Site,
                    `H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    Affiliate,
                    ETC,
                    `Customer Sub Status`,
                    `Accounts Changed`,
                    `Net Revenue`,
                    `Accounts Changed All`,
                    `Activity Base`
                    
                FROM 
                    {query_right}
                """
            return union_df
        except Exception as err:
            print("Error: union_df", err)
            
    def union_df_res_date_2020_false(union_df):
        try:
            union_df_res_date_2020_false = f"""
                    SELECT 
                    Date,
                    `Channel Group`,
                    Channel,
                    Activity,
                    `Sub Channel`,
                    Site,
                    `H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    Affiliate,
                    ETC,
                    `Customer Sub Status`,
                    CASE 
                        WHEN ISNULL(`Accounts Changed`) THEN 0 ELSE `Accounts Changed` END AS `Accounts Changed`,
                    CASE 
                        WHEN ISNULL(`Net Revenue`) THEN 0 ELSE `Net Revenue` END AS `Net Revenue`,
                    CASE 
                        WHEN `Activity` IN ('New Connect', 'Restart') THEN 'New Connect' 
                        WHEN `Activity` IN ('Uptier', 'Upgrade') THEN '+ Base' 
                        WHEN `Activity` IN ('Downtier', 'Downgrade') THEN '- Base' 
                        WHEN `Activity` = 'Transfer' THEN 'Transfer' 
                        WHEN `Activity` = 'Disconnect' THEN 'Disconnect' 
                        ELSE `Activity` 
                    END AS `Activity Base`,
                    CASE 
                        WHEN `Date` >= '2020-01-01' AND `Date` <= '2020-12-31' THEN 1 
                        ELSE 0 
                    END AS `DateCondition`
                FROM 
                    {union_df}
                WHERE 

                    NOT (Date >= '2020-01-01' AND Date <= '2020-12-31') 
                    AND NOT (Date >= '2018-12-31' AND Date <= '2020-01-01'); 
                """
            return union_df_res_date_2020_false
        except Exception as err:
            print("Error: union_df_res_date_2020_false", err)
            
    def union_df_res_date_2020_true(union_df):
        try:
            union_df_res_date_2020_true = f"""
                    SELECT 
                    Date,
                    `Channel Group`,
                    Channel,
                    Activity,
                    `Sub Channel`,
                    Site,
                    `H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    Affiliate,
                    ETC,
                    `Customer Sub Status`,
                    CASE 
                        WHEN ISNULL(`Accounts Changed`) THEN 0 ELSE `Accounts Changed` END AS `Accounts Changed`,
                    CASE 
                        WHEN ISNULL(`Net Revenue`) THEN 0 ELSE `Net Revenue` END AS `Net Revenue`,
                    CASE 
                        WHEN `Activity` IN ('New Connect', 'Restart') THEN 'New Connect' 
                        WHEN `Activity` IN ('Uptier', 'Upgrade') THEN '+ Base' 
                        WHEN `Activity` IN ('Downtier', 'Downgrade') THEN '- Base' 
                        WHEN `Activity` = 'Transfer' THEN 'Transfer' 
                        WHEN `Activity` = 'Disconnect' THEN 'Disconnect' 
                        ELSE `Activity` 
                    END AS `Activity Base`,
                    CASE 
                        WHEN `Date` >= '2020-01-01' AND `Date` <= '2020-12-31' THEN 1 
                        ELSE 0 
                    END AS `DateCondition`
                FROM 
                    {union_df}
                WHERE 

                    (Date >= '2020-01-01' AND Date <= '2020-12-31')  
                """
            return union_df_res_date_2020_true
        except Exception as err:
            print("Error: union_df_res_date_2020_true", err)
            
    def union_df_res_date_2019_true(union_df):
        try:
            union_df_res_date_2019_true = f"""
                    SELECT 
                    Date,
                    `Channel Group`,
                    Channel,
                    Activity,
                    `Sub Channel`,
                    Site,
                    `H Channel Group`,
                    `H Channel`,
                    `H ETC`,
                    Affiliate,
                    ETC,
                    `Customer Sub Status`,
                    CASE 
                        WHEN ISNULL(`Accounts Changed`) THEN 0 ELSE `Accounts Changed` END AS `Accounts Changed`,
                    CASE 
                        WHEN ISNULL(`Net Revenue`) THEN 0 ELSE `Net Revenue` END AS `Net Revenue`,
                    CASE 
                        WHEN `Activity` IN ('New Connect', 'Restart') THEN 'New Connect' 
                        WHEN `Activity` IN ('Uptier', 'Upgrade') THEN '+ Base' 
                        WHEN `Activity` IN ('Downtier', 'Downgrade') THEN '- Base' 
                        WHEN `Activity` = 'Transfer' THEN 'Transfer' 
                        WHEN `Activity` = 'Disconnect' THEN 'Disconnect' 
                        ELSE `Activity` 
                    END AS `Activity Base`,
                    CASE 
                        WHEN `Date` >= '2020-01-01' AND `Date` <= '2020-12-31' THEN 1 
                        ELSE 0 
                    END AS `DateCondition`
                FROM 
                    {union_df}
                WHERE 

                    NOT (Date >= '2020-01-01' AND Date <= '2020-12-31') 
                    AND (Date >= '2018-12-31' AND Date <= '2020-01-01')
                """
            return union_df_res_date_2019_true
        except Exception as err:
            print("Error: union_df_res_date_2019_true", err)
            
    def joined_df_holidays(union_df_res_date_2020_true,df_holidays):
        try:
            joined_df_holidays = f"""
                    SELECT 
                    u.Date,
                    u.`Channel Group`,
                    u.Channel,
                    u.Activity,
                    u.`Activity Base`,        
                    u.`Accounts Changed`,
                    u.`Net Revenue`
                FROM 
                    union_df_res_date_2020_true u
                LEFT JOIN 
                    df_holidays h
                ON 
                    u.Date = h.Date
                """
            return joined_df_holidays
        except Exception as err:
            print("Error: joined_df_holidays", err)
       
        