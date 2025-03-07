from pyspark.sql import SparkSession, DataFrame

class NRPA:

    def process_data(self, spark:SparkSession)->DataFrame:

        net_revenue_query = """"SELECT
        swodf_f.TIME_KEY
        ,swodf_f.COX_ID_DTL_BILLING_KEY
        ,swodf_f.COX_ID_DTL_HR_KEY
        ,swodf_f.COX_ID_DTL_SITE_KEY
        ,swodf_f.SALES_CHANNEL_HIER_KEY
        ,swodf_f.CS_AGENT_HIER_DLY_KEY
        ,swodf_f.CS_AGENT_HIER_MTHLY_KEY
        ,swodf_f.CUSTOMER_SUBSTATUS_KEY
        ,swodf_f.SITE_KEY
        ,swodf_f.ACCNT_NBR
        ,swodf_f.CUSTOMER_KEY
        ,swodf_f.WO_NBR
        ,swodf_f.WO_TYPE_DESC
        ,swodf_f.TRANSFERRED_FLG
        ,swodf_f.ACTIVITY
        ,SUM(swodf_f.TOTAL_NET_REV) AS TOTAL_NET_REV
        ,SUM(swodf_f.ACCT_CHANGE_CNT) AS ACCT_CHANGE_CNT
        ,MAX(swodf_f.PSU_CONNECT) AS PSU_CONNECT
        ,MAX(swodf_f.PSU_DISCONNECT) AS PSU_DISCONNECT
FROM    (
SELECT  cdns.TIME_KEY
        ,cdns.COX_ID_DTL_BILLING_KEY
        ,cdns.COX_ID_DTL_HR_KEY
        ,cdns.COX_ID_DTL_SITE_KEY
        ,cdns.SALES_CHANNEL_HIER_KEY
        ,cdns.CS_AGENT_HIER_DLY_KEY
        ,cdns.CS_AGENT_HIER_MTHLY_KEY
        ,cdns.CUSTOMER_SUBSTATUS_KEY
        ,cdns.CUSTOMER_KEY
        ,cdns.SITE_KEY
        ,cdns.ACCNT_NBR
        ,cdns.WO_NBR
        ,cdns.WO_TYPE_DESC
        ,cdns.TRANSFERRED_FLG
        ,CASE WHEN cdns.WO_TYPE_DESC = 'Disconnect' THEN 'Disconnect'
              WHEN cdns.WO_TYPE_DESC = 'Restart' THEN 'Restart'
              WHEN cdns.WO_TYPE_DESC = 'Install' and cdns.CUSTOMER_SUBSTATUS_KEY in (2,8) and CDNS.SERVICE_NEW_QTY > 0 THEN 'New_Connect'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 0 THEN 'Upgrade'
              WHEN cdns.PSU_CONNECT = 0 AND cdns.PSU_DISCONNECT = 1 THEN 'Downgrade'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 1 AND cdns.PSU_NEW_QTY > cdns.PSU_OLD_QTY THEN 'Upgrade'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 1 AND cdns.PSU_NEW_QTY < cdns.PSU_OLD_QTY THEN 'Downgrade'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 1 AND cdns.PSU_NEW_QTY = cdns.PSU_OLD_QTY THEN 'Sidegrade'
              WHEN cdns.PSU_CONNECT = 0 AND cdns.PSU_DISCONNECT = 0 AND cdns.TOTAL_NET_REV > 0 THEN 'Uptier'
              WHEN cdns.PSU_CONNECT = 0 AND cdns.PSU_DISCONNECT = 0 AND cdns.TOTAL_NET_REV < 0 THEN 'Downtier'
              --No Change and No Revenue logic: MRB
              WHEN cdns.SERVICE_NEW_QTY = 0 AND cdns.SERVICE_OLD_QTY = 0 AND cdns.TOTAL_NET_REV = 0 THEN 'None'
              ELSE 'Other' END AS ACTIVITY
        ,SUM(cdns.TOTAL_NET_REV) AS TOTAL_NET_REV
        ,COUNT(DISTINCT (cdns.ACCT_CHNG)) AS ACCT_CHANGE_CNT
        ,MAX(cdns.PSU_CONNECT) AS PSU_CONNECT
        ,MAX(cdns.PSU_DISCONNECT) AS PSU_DISCONNECT
FROM   (
SELECT  cdn.TIME_KEY
        ,cdn.COX_ID_DTL_BILLING_KEY
        ,cdn.COX_ID_DTL_HR_KEY
        ,cdn.COX_ID_DTL_SITE_KEY
        ,cdn.SALES_CHANNEL_HIER_KEY
        ,cdn.CS_AGENT_HIER_DLY_KEY
        ,cdn.CS_AGENT_HIER_MTHLY_KEY
        ,cdn.CUSTOMER_SUBSTATUS_KEY
        ,cdn.ACCNT_NBR
        ,cdn.WO_NBR
        ,cdn.CUSTOMER_KEY
        ,cdn.SITE_KEY
        ,cdn.WO_TYPE_DESC
        ,cdn.TRANSFERRED_FLG
        ,MAX(cdn.PSU_CONNECTS) AS PSU_CONNECT
        ,MAX(cdn.PSU_DISCONNECTS) AS PSU_DISCONNECT
        ,SUM(cdn.PSU_OLD_QTY) AS PSU_OLD_QTY
        ,SUM(cdn.PSU_NEW_QTY) AS PSU_NEW_QTY
        ,SUM(cdn.SERVICE_OLD_QTY) AS SERVICE_OLD_QTY
        ,SUM(cdn.SERVICE_NEW_QTY) AS SERVICE_NEW_QTY
        ,SUM(cdn.NET_REVENUE) AS TOTAL_NET_REV
        ,cdn.ACCT_CHNG
FROM   (
SELECT  camcid.TIME_KEY
        ,camcid.HYBRID_COX_ID_BILLING_KEY
        ,camcid.COX_ID_DTL_BILLING_KEY
        ,camcid.COX_ID_DTL_HR_KEY
        ,camcid.COX_ID_DTL_SITE_KEY
        ,scd.SALES_CHANNEL_HIER_KEY
        ,camcid.CS_AGENT_HIER_DLY_KEY
        ,camcid.CS_AGENT_HIER_MTHLY_KEY
        ,camcid.CUSTOMER_SUBSTATUS_KEY
        ,camcid.ACCNT_NBR
        ,camcid.WO_NBR
        ,camcid.CUSTOMER_KEY
        ,camcid.SITE_KEY
        ,pd.REPORTING_PRODUCT_FLAG
        ,pd.PRODUCT_CATEGORY_CD
        ,ot.OUTLET_TYPE_CD
        ,wtd.WO_TYPE_DESC
        ,NVL(camcid.TRANSFERRED_FLG, 'N') AS TRANSFERRED_FLG
        ,SUM(CASE WHEN camcid.OLD_SERVICE_QTY > 0 AND pd.REPORTING_PRODUCT_FLAG IN('Basic', 'Data', 'Home_Sec', 'Telephony') AND ot.OUTLET_TYPE_CD = 'P' THEN camcid.OLD_SERVICE_QTY ELSE 0 END) AS PSU_OLD_QTY
        ,SUM(CASE WHEN camcid.NEW_SERVICE_QTY > 0 AND pd.REPORTING_PRODUCT_FLAG IN('Basic', 'Data', 'Home_Sec', 'Telephony') AND ot.OUTLET_TYPE_CD = 'P' THEN camcid.NEW_SERVICE_QTY ELSE 0 END) AS PSU_NEW_QTY
        ,SUM(CASE WHEN camcid.OLD_SERVICE_QTY > 0 THEN camcid.OLD_SERVICE_QTY ELSE 0 END) AS SERVICE_OLD_QTY
        ,SUM(CASE WHEN camcid.NEW_SERVICE_QTY > 0 THEN camcid.NEW_SERVICE_QTY ELSE 0 END) AS SERVICE_NEW_QTY
        ,SUM(camcid.PSU_CONNECTS_CNT) AS PSU_CONNECTS
        ,SUM(camcid.PSU_DISCONNECTS_CNT) AS PSU_DISCONNECTS
        ,SUM((camcid.CONN_NEW_RT_AMT - camcid.CONN_OLD_RT_AMT) + (camcid.DISC_NEW_RT_AMT - camcid.DISC_OLD_RT_AMT) + (camcid.NOCHG_NEW_RT_AMT - camcid.NOCHG_OLD_RT_AMT) + (camcid.CONN_OLD_RTAIN_CAMP_DISCNT_AMT - camcid.CONN_NEW_RTAIN_CAMP_DISCNT_AMT) + (camcid.CONN_OLD_OTH_CAMP_DISCNT_AMT - camcid.CONN_NEW_OTH_CAMP_DISCNT_AMT) + (camcid.DISC_OLD_RTAIN_CAMP_DISCNT_AMT - camcid.DISC_NEW_RTAIN_CAMP_DISCNT_AMT) + (camcid.DISC_OLD_OTH_CAMP_DISCNT_AMT - camcid.DISC_NEW_OTH_CAMP_DISCNT_AMT) + (camcid.NOCHG_OLD_RTAN_CAMP_DISCNT_AMT - camcid.NOCHG_NEW_RTAN_CAMP_DISCNT_AMT) + (camcid.NOCHG_OLD_OTH_CAMP_DISCNT_AMT - camcid.NOCHG_NEW_OTH_CAMP_DISCNT_AMT) + (camcid.CONN_OLD_PKG_DISCNT_AMT - camcid.CONN_NEW_PKG_DISCNT_AMT) + (camcid.DISC_OLD_PKG_DISCNT_AMT - camcid.DISC_NEW_PKG_DISCNT_AMT) + (camcid.NOCHG_OLD_PKG_DISCNT_AMT - camcid.NOCHG_NEW_PKG_DISCNT_AMT)) AS NET_REVENUE
        ,camcid.TIME_KEY || camcid.CUSTOMER_KEY || camcid.HYBRID_COX_ID_BILLING_KEY as ACCT_CHNG
FROM    MSADMIN.CS_AGENT_METRIC_CHK_IN_DTL_V camcid
        INNER JOIN EDW.PRODUCT_DIM pd
          ON camcid.PRODUCT_KEY = pd.PRODUCT_KEY
        INNER JOIN EDW.WO_TYPE_DIM wtd
          ON camcid.WO_TYPE_KEY = wtd.WO_TYPE_KEY
        INNER JOIN EDW.CUSTOMER_SUBSTATUS_DIM csd
          ON camcid.CUSTOMER_SUBSTATUS_KEY = csd.CUSTOMER_SUBSTATUS_KEY
        INNER JOIN EDW.SALES_CHANNEL_DIM scd
          ON camcid.CNCT_SALES_CHANNEL_KEY = scd.SALES_CHANNEL_KEY
        INNER JOIN EDW.OUTLET_TYPE_DIM ot ON ot.OUTLET_TYPE_KEY = camcid.OUTLET_TYPE_KEY
WHERE  camcid.TIME_KEY BETWEEN (current_date-36) AND (current_date-1)
        and camcid.WO_STATUS_KEY = 1
        and camcid.BILL_TYPE_KEY = 1
        and WTD.WO_TYPE_CD NOT IN ('SR', 'TC', 'NP')
GROUP BY camcid.TIME_KEY
        ,camcid.HYBRID_COX_ID_BILLING_KEY
        ,camcid.COX_ID_DTL_BILLING_KEY
        ,camcid.COX_ID_DTL_HR_KEY
        ,camcid.COX_ID_DTL_SITE_KEY
        ,scd.SALES_CHANNEL_HIER_KEY
        ,camcid.CS_AGENT_HIER_DLY_KEY
        ,camcid.CS_AGENT_HIER_MTHLY_KEY
        ,camcid.CUSTOMER_SUBSTATUS_KEY
        ,camcid.ACCNT_NBR
        ,camcid.WO_NBR
        ,camcid.CUSTOMER_KEY
        ,camcid.SITE_KEY
        ,pd.REPORTING_PRODUCT_FLAG
        ,pd.PRODUCT_CATEGORY_CD
        ,ot.OUTLET_TYPE_CD
        ,wtd.WO_TYPE_DESC
        ,NVL(camcid.TRANSFERRED_FLG, 'N')
) cdn
GROUP BY
        cdn.TIME_KEY
        ,cdn.COX_ID_DTL_BILLING_KEY
        ,cdn.COX_ID_DTL_HR_KEY
        ,cdn.COX_ID_DTL_SITE_KEY
        ,cdn.SALES_CHANNEL_HIER_KEY
        ,cdn.CS_AGENT_HIER_DLY_KEY
        ,cdn.CS_AGENT_HIER_MTHLY_KEY
        ,cdn.CUSTOMER_SUBSTATUS_KEY
        ,cdn.ACCNT_NBR
        ,cdn.WO_NBR
        ,cdn.CUSTOMER_KEY
        ,cdn.SITE_KEY
        ,cdn.WO_TYPE_DESC
        ,cdn.TRANSFERRED_FLG
        ,cdn.ACCT_CHNG
) cdns
GROUP BY
        cdns.TIME_KEY
        ,cdns.COX_ID_DTL_BILLING_KEY
        ,cdns.COX_ID_DTL_HR_KEY
        ,cdns.COX_ID_DTL_SITE_KEY
        ,cdns.SALES_CHANNEL_HIER_KEY
        ,cdns.CS_AGENT_HIER_DLY_KEY
        ,cdns.CS_AGENT_HIER_MTHLY_KEY
        ,cdns.CUSTOMER_SUBSTATUS_KEY
        ,cdns.CUSTOMER_KEY
        ,cdns.SITE_KEY
        ,cdns.ACCNT_NBR
        ,cdns.WO_NBR
        ,cdns.WO_TYPE_DESC
        ,cdns.TRANSFERRED_FLG
        ,CASE WHEN cdns.WO_TYPE_DESC = 'Disconnect' THEN 'Disconnect'
              WHEN cdns.WO_TYPE_DESC = 'Restart' THEN 'Restart'
              WHEN cdns.WO_TYPE_DESC = 'Install' and cdns.CUSTOMER_SUBSTATUS_KEY in (2,8) and CDNS.SERVICE_NEW_QTY > 0 THEN 'New_Connect'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 0 THEN 'Upgrade'
              WHEN cdns.PSU_CONNECT = 0 AND cdns.PSU_DISCONNECT = 1 THEN 'Downgrade'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 1 AND cdns.PSU_NEW_QTY > cdns.PSU_OLD_QTY THEN 'Upgrade'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 1 AND cdns.PSU_NEW_QTY < cdns.PSU_OLD_QTY THEN 'Downgrade'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 1 AND cdns.PSU_NEW_QTY = cdns.PSU_OLD_QTY THEN 'Sidegrade'
              WHEN cdns.PSU_CONNECT = 0 AND cdns.PSU_DISCONNECT = 0 AND cdns.TOTAL_NET_REV > 0 THEN 'Uptier'
              WHEN cdns.PSU_CONNECT = 0 AND cdns.PSU_DISCONNECT = 0 AND cdns.TOTAL_NET_REV < 0 THEN 'Downtier'
              --No Change and No Revenue logic: MRB
              WHEN cdns.SERVICE_NEW_QTY = 0 AND cdns.SERVICE_OLD_QTY = 0 AND cdns.TOTAL_NET_REV = 0 THEN 'None'
              ELSE 'Other' END
        ,CASE WHEN cdns.TOTAL_NET_REV < 0 THEN 1 ELSE 0 END
) swodf_f
GROUP BY
        swodf_f.TIME_KEY
        ,swodf_f.COX_ID_DTL_BILLING_KEY
        ,swodf_f.COX_ID_DTL_HR_KEY
        ,swodf_f.COX_ID_DTL_SITE_KEY
        ,swodf_f.SALES_CHANNEL_HIER_KEY
        ,swodf_f.CS_AGENT_HIER_DLY_KEY
        ,swodf_f.CS_AGENT_HIER_MTHLY_KEY
        ,swodf_f.CUSTOMER_SUBSTATUS_KEY
        ,swodf_f.SITE_KEY
        ,swodf_f.ACCNT_NBR
        ,swodf_f.CUSTOMER_KEY
        ,swodf_f.WO_NBR
        ,swodf_f.WO_TYPE_DESC
        ,swodf_f.TRANSFERRED_FLG
        ,swodf_f.ACTIVITY
        """

        psus_query = """SELECT 
        swodf_f.TIME_KEY
        ,swodf_f.COX_ID_DTL_BILLING_KEY
        ,swodf_f.COX_ID_DTL_HR_KEY
        ,swodf_f.COX_ID_DTL_SITE_KEY
        ,swodf_f.SALES_CHANNEL_HIER_KEY
        ,swodf_f.CS_AGENT_HIER_DLY_KEY
        ,swodf_f.CS_AGENT_HIER_MTHLY_KEY
        ,swodf_f.CUSTOMER_SUBSTATUS_KEY
        ,swodf_f.SITE_KEY
        ,swodf_f.ACCNT_NBR
        ,swodf_f.CUSTOMER_KEY
        ,swodf_f.WO_NBR
        ,swodf_f.WO_TYPE_DESC
        ,swodf_f.TRANSFERRED_FLG
        ,swodf_f.ACTIVITY
        ,SUM(swodf_f.TOTAL_NET_REV) AS TOTAL_NET_REV
        ,SUM(swodf_f.ACCT_CHANGE_CNT) AS ACCT_CHANGE_CNT
        ,SUM(swodf_f.PSU_CONNECT) AS PSU_CONNECT
        ,SUM(swodf_f.PSU_DISCONNECT) AS PSU_DISCONNECT
FROM    (
SELECT  cdns.TIME_KEY
        ,cdns.COX_ID_DTL_BILLING_KEY
        ,cdns.COX_ID_DTL_HR_KEY
        ,cdns.COX_ID_DTL_SITE_KEY
        ,cdns.SALES_CHANNEL_HIER_KEY
        ,cdns.CS_AGENT_HIER_DLY_KEY
        ,cdns.CS_AGENT_HIER_MTHLY_KEY
        ,cdns.CUSTOMER_SUBSTATUS_KEY
        ,cdns.CUSTOMER_KEY
        ,cdns.SITE_KEY
        ,cdns.ACCNT_NBR
        ,cdns.WO_NBR
        ,cdns.WO_TYPE_DESC
        ,cdns.TRANSFERRED_FLG
        ,CASE WHEN cdns.WO_TYPE_DESC = 'Disconnect' THEN 'Disconnect'
              WHEN cdns.WO_TYPE_DESC = 'Restart' THEN 'Restart'
              WHEN cdns.WO_TYPE_DESC = 'Install' and cdns.CUSTOMER_SUBSTATUS_KEY in (2,8) and CDNS.SERVICE_NEW_QTY > 0 THEN 'New_Connect'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 0 THEN 'Upgrade'
              WHEN cdns.PSU_CONNECT = 0 AND cdns.PSU_DISCONNECT = 1 THEN 'Downgrade'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 1 AND cdns.PSU_NEW_QTY > cdns.PSU_OLD_QTY THEN 'Upgrade'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 1 AND cdns.PSU_NEW_QTY < cdns.PSU_OLD_QTY THEN 'Downgrade'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 1 AND cdns.PSU_NEW_QTY = cdns.PSU_OLD_QTY THEN 'Sidegrade'
              WHEN cdns.PSU_CONNECT = 0 AND cdns.PSU_DISCONNECT = 0 AND cdns.TOTAL_NET_REV > 0 THEN 'Uptier'
              WHEN cdns.PSU_CONNECT = 0 AND cdns.PSU_DISCONNECT = 0 AND cdns.TOTAL_NET_REV < 0 THEN 'Downtier'
              --No Change and No Revenue logic: MRB
              WHEN cdns.SERVICE_NEW_QTY = 0 AND cdns.SERVICE_OLD_QTY = 0 AND cdns.TOTAL_NET_REV = 0 THEN 'None'
              ELSE 'Other' END AS ACTIVITY
        ,SUM(cdns.TOTAL_NET_REV) AS TOTAL_NET_REV
        ,COUNT(DISTINCT (cdns.ACCT_CHNG)) AS ACCT_CHANGE_CNT
        ,SUM(cdns.PSU_CONNECT) AS PSU_CONNECT
        ,SUM(cdns.PSU_DISCONNECT) AS PSU_DISCONNECT
FROM   (
SELECT  cdn.TIME_KEY
        ,cdn.COX_ID_DTL_BILLING_KEY
        ,cdn.COX_ID_DTL_HR_KEY
        ,cdn.COX_ID_DTL_SITE_KEY
        ,cdn.SALES_CHANNEL_HIER_KEY
        ,cdn.CS_AGENT_HIER_DLY_KEY
        ,cdn.CS_AGENT_HIER_MTHLY_KEY
        ,cdn.CUSTOMER_SUBSTATUS_KEY
        ,cdn.ACCNT_NBR
        ,cdn.WO_NBR
        ,cdn.CUSTOMER_KEY
        ,cdn.SITE_KEY
        ,cdn.WO_TYPE_DESC
        ,cdn.TRANSFERRED_FLG
        ,SUM(cdn.PSU_CONNECTS) AS PSU_CONNECT
        ,SUM(cdn.PSU_DISCONNECTS) AS PSU_DISCONNECT
        ,SUM(cdn.PSU_OLD_QTY) AS PSU_OLD_QTY
        ,SUM(cdn.PSU_NEW_QTY) AS PSU_NEW_QTY
        ,SUM(cdn.SERVICE_OLD_QTY) AS SERVICE_OLD_QTY
        ,SUM(cdn.SERVICE_NEW_QTY) AS SERVICE_NEW_QTY
        ,SUM(cdn.NET_REVENUE) AS TOTAL_NET_REV
        ,cdn.ACCT_CHNG
FROM   (
SELECT  camcid.TIME_KEY
        ,camcid.HYBRID_COX_ID_BILLING_KEY
        ,camcid.COX_ID_DTL_BILLING_KEY
        ,camcid.COX_ID_DTL_HR_KEY
        ,camcid.COX_ID_DTL_SITE_KEY
        ,scd.SALES_CHANNEL_HIER_KEY
        ,camcid.CS_AGENT_HIER_DLY_KEY
        ,camcid.CS_AGENT_HIER_MTHLY_KEY
        ,camcid.CUSTOMER_SUBSTATUS_KEY
        ,camcid.ACCNT_NBR
        ,camcid.WO_NBR
        ,camcid.CUSTOMER_KEY
        ,camcid.SITE_KEY
        ,pd.REPORTING_PRODUCT_FLAG
        ,pd.PRODUCT_CATEGORY_CD
        ,ot.OUTLET_TYPE_CD
        ,wtd.WO_TYPE_DESC
        ,NVL(camcid.TRANSFERRED_FLG, 'N') AS TRANSFERRED_FLG
        ,SUM(CASE WHEN camcid.OLD_SERVICE_QTY > 0 AND pd.REPORTING_PRODUCT_FLAG IN('Basic', 'Data', 'Home_Sec', 'Telephony') AND ot.OUTLET_TYPE_CD = 'P' THEN camcid.OLD_SERVICE_QTY ELSE 0 END) AS PSU_OLD_QTY
        ,SUM(CASE WHEN camcid.NEW_SERVICE_QTY > 0 AND pd.REPORTING_PRODUCT_FLAG IN('Basic', 'Data', 'Home_Sec', 'Telephony') AND ot.OUTLET_TYPE_CD = 'P' THEN camcid.NEW_SERVICE_QTY ELSE 0 END) AS PSU_NEW_QTY
        ,SUM(CASE WHEN camcid.OLD_SERVICE_QTY > 0 THEN camcid.OLD_SERVICE_QTY ELSE 0 END) AS SERVICE_OLD_QTY
        ,SUM(CASE WHEN camcid.NEW_SERVICE_QTY > 0 THEN camcid.NEW_SERVICE_QTY ELSE 0 END) AS SERVICE_NEW_QTY
        ,SUM(camcid.PSU_CONNECTS_CNT) AS PSU_CONNECTS
        ,SUM(camcid.PSU_DISCONNECTS_CNT) AS PSU_DISCONNECTS
        ,SUM((camcid.CONN_NEW_RT_AMT - camcid.CONN_OLD_RT_AMT) + (camcid.DISC_NEW_RT_AMT - camcid.DISC_OLD_RT_AMT) + (camcid.NOCHG_NEW_RT_AMT - camcid.NOCHG_OLD_RT_AMT) + (camcid.CONN_OLD_RTAIN_CAMP_DISCNT_AMT - camcid.CONN_NEW_RTAIN_CAMP_DISCNT_AMT) + (camcid.CONN_OLD_OTH_CAMP_DISCNT_AMT - camcid.CONN_NEW_OTH_CAMP_DISCNT_AMT) + (camcid.DISC_OLD_RTAIN_CAMP_DISCNT_AMT - camcid.DISC_NEW_RTAIN_CAMP_DISCNT_AMT) + (camcid.DISC_OLD_OTH_CAMP_DISCNT_AMT - camcid.DISC_NEW_OTH_CAMP_DISCNT_AMT) + (camcid.NOCHG_OLD_RTAN_CAMP_DISCNT_AMT - camcid.NOCHG_NEW_RTAN_CAMP_DISCNT_AMT) + (camcid.NOCHG_OLD_OTH_CAMP_DISCNT_AMT - camcid.NOCHG_NEW_OTH_CAMP_DISCNT_AMT) + (camcid.CONN_OLD_PKG_DISCNT_AMT - camcid.CONN_NEW_PKG_DISCNT_AMT) + (camcid.DISC_OLD_PKG_DISCNT_AMT - camcid.DISC_NEW_PKG_DISCNT_AMT) + (camcid.NOCHG_OLD_PKG_DISCNT_AMT - camcid.NOCHG_NEW_PKG_DISCNT_AMT)) AS NET_REVENUE
        ,camcid.TIME_KEY || camcid.CUSTOMER_KEY || camcid.HYBRID_COX_ID_BILLING_KEY as ACCT_CHNG
FROM    MSADMIN.CS_AGENT_METRIC_CHK_IN_DTL_V camcid
        INNER JOIN EDW.PRODUCT_DIM pd
          ON camcid.PRODUCT_KEY = pd.PRODUCT_KEY
        INNER JOIN EDW.WO_TYPE_DIM wtd
          ON camcid.WO_TYPE_KEY = wtd.WO_TYPE_KEY
        INNER JOIN EDW.CUSTOMER_SUBSTATUS_DIM csd
          ON camcid.CUSTOMER_SUBSTATUS_KEY = csd.CUSTOMER_SUBSTATUS_KEY
        INNER JOIN EDW.SALES_CHANNEL_DIM scd
          ON camcid.CNCT_SALES_CHANNEL_KEY = scd.SALES_CHANNEL_KEY
        INNER JOIN EDW.OUTLET_TYPE_DIM ot ON ot.OUTLET_TYPE_KEY = camcid.OUTLET_TYPE_KEY
WHERE   camcid.TIME_KEY BETWEEN (current_date-36) AND (current_date-1)
        and camcid.WO_STATUS_KEY = 1
        and camcid.BILL_TYPE_KEY = 1
        and WTD.WO_TYPE_CD NOT IN ('SR', 'TC', 'NP')
GROUP BY camcid.TIME_KEY
        ,camcid.HYBRID_COX_ID_BILLING_KEY
        ,camcid.COX_ID_DTL_BILLING_KEY
        ,camcid.COX_ID_DTL_HR_KEY
        ,camcid.COX_ID_DTL_SITE_KEY
        ,scd.SALES_CHANNEL_HIER_KEY
        ,camcid.CS_AGENT_HIER_DLY_KEY
        ,camcid.CS_AGENT_HIER_MTHLY_KEY
        ,camcid.CUSTOMER_SUBSTATUS_KEY
        ,camcid.ACCNT_NBR
        ,camcid.WO_NBR
        ,camcid.CUSTOMER_KEY
        ,camcid.SITE_KEY
        ,pd.REPORTING_PRODUCT_FLAG
        ,pd.PRODUCT_CATEGORY_CD
        ,ot.OUTLET_TYPE_CD
        ,wtd.WO_TYPE_DESC
        ,NVL(camcid.TRANSFERRED_FLG, 'N')
) cdn
GROUP BY
        cdn.TIME_KEY
        ,cdn.COX_ID_DTL_BILLING_KEY
        ,cdn.COX_ID_DTL_HR_KEY
        ,cdn.COX_ID_DTL_SITE_KEY
        ,cdn.SALES_CHANNEL_HIER_KEY
        ,cdn.CS_AGENT_HIER_DLY_KEY
        ,cdn.CS_AGENT_HIER_MTHLY_KEY
        ,cdn.CUSTOMER_SUBSTATUS_KEY
        ,cdn.ACCNT_NBR
        ,cdn.WO_NBR
        ,cdn.CUSTOMER_KEY
        ,cdn.SITE_KEY
        ,cdn.WO_TYPE_DESC
        ,cdn.TRANSFERRED_FLG
        ,cdn.ACCT_CHNG
) cdns
GROUP BY
        cdns.TIME_KEY
        ,cdns.COX_ID_DTL_BILLING_KEY
        ,cdns.COX_ID_DTL_HR_KEY
        ,cdns.COX_ID_DTL_SITE_KEY
        ,cdns.SALES_CHANNEL_HIER_KEY
        ,cdns.CS_AGENT_HIER_DLY_KEY
        ,cdns.CS_AGENT_HIER_MTHLY_KEY
        ,cdns.CUSTOMER_SUBSTATUS_KEY
        ,cdns.CUSTOMER_KEY
        ,cdns.SITE_KEY
        ,cdns.ACCNT_NBR
        ,cdns.WO_NBR
        ,cdns.WO_TYPE_DESC
        ,cdns.TRANSFERRED_FLG
        ,CASE WHEN cdns.WO_TYPE_DESC = 'Disconnect' THEN 'Disconnect'
              WHEN cdns.WO_TYPE_DESC = 'Restart' THEN 'Restart'
              WHEN cdns.WO_TYPE_DESC = 'Install' and cdns.CUSTOMER_SUBSTATUS_KEY in (2,8) and CDNS.SERVICE_NEW_QTY > 0 THEN 'New_Connect'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 0 THEN 'Upgrade'
              WHEN cdns.PSU_CONNECT = 0 AND cdns.PSU_DISCONNECT = 1 THEN 'Downgrade'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 1 AND cdns.PSU_NEW_QTY > cdns.PSU_OLD_QTY THEN 'Upgrade'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 1 AND cdns.PSU_NEW_QTY < cdns.PSU_OLD_QTY THEN 'Downgrade'
              WHEN cdns.PSU_CONNECT = 1 AND cdns.PSU_DISCONNECT = 1 AND cdns.PSU_NEW_QTY = cdns.PSU_OLD_QTY THEN 'Sidegrade'
              WHEN cdns.PSU_CONNECT = 0 AND cdns.PSU_DISCONNECT = 0 AND cdns.TOTAL_NET_REV > 0 THEN 'Uptier'
              WHEN cdns.PSU_CONNECT = 0 AND cdns.PSU_DISCONNECT = 0 AND cdns.TOTAL_NET_REV < 0 THEN 'Downtier'
              --No Change and No Revenue logic: MRB
              WHEN cdns.SERVICE_NEW_QTY = 0 AND cdns.SERVICE_OLD_QTY = 0 AND cdns.TOTAL_NET_REV = 0 THEN 'None'
              ELSE 'Other' END
        ,CASE WHEN cdns.TOTAL_NET_REV < 0 THEN 1 ELSE 0 END
) swodf_f
GROUP BY
        swodf_f.TIME_KEY
        ,swodf_f.COX_ID_DTL_BILLING_KEY
        ,swodf_f.COX_ID_DTL_HR_KEY
        ,swodf_f.COX_ID_DTL_SITE_KEY
        ,swodf_f.SALES_CHANNEL_HIER_KEY
        ,swodf_f.CS_AGENT_HIER_DLY_KEY
        ,swodf_f.CS_AGENT_HIER_MTHLY_KEY
        ,swodf_f.CUSTOMER_SUBSTATUS_KEY
        ,swodf_f.SITE_KEY
        ,swodf_f.ACCNT_NBR
        ,swodf_f.CUSTOMER_KEY
        ,swodf_f.WO_NBR
        ,swodf_f.WO_TYPE_DESC
        ,swodf_f.TRANSFERRED_FLG
        ,swodf_f.ACTIVITY
        """

        schd_query = """SELECT
        SALES_CHANNEL_HIER_KEY,
        EMPLOYEE_TYPE_CD,
        SALES_CHANNEL_GROUP_NM,
        SALES_CHANNEL_NM,
        SALES_SUB_CHANNEL_NM,
        AFFILIATE_NM,
        DISPLAY_CHANNEL_GROUP_NM 
    FROM EDW.SALES_CHANNEL_HIER_DIM"""

        customer_sub_status_query = """SELECT
        CUSTOMER_SUBSTATUS_KEY,
        SUB_STATUS_DESC
    FROM EDW.CUSTOMER_SUBSTATUS_DIM"""

        site_dim_query = """SELECT 
        SITE_KEY,
        SITE_DESC,
        SITE_ID

        FROM SIW.DIM_SITE"""

        final_query = f"""
        with

        NET_REVENUE AS ({net_revenue_query}),

        PSUS AS ({psus_query}),

        SCHD AS ({schd_query}),

        CUSTOMER_SUB_STATUS AS ({customer_sub_status_query}),

        SITE_DIM AS ({site_dim_query}),

        JOINED_NRPA AS (
        SELECT
            nr.time_key,
            nr.COX_ID_DTL_BILLING_KEY,
            nr.COX_ID_DTL_HR_KEY,
            nr.COX_ID_DTL_SITE_KEY,
            nr.SALES_CHANNEL_HIER_KEY,
            nr.CS_AGENT_HIER_DLY_KEY,
            nr.CS_AGENT_HIER_MTHLY_KEY,
            nr.CUSTOMER_SUBSTATUS_KEY,
            nr.SITE_KEY,
            nr.ACCNT_NBR,
            nr.CUSTOMER_KEY,
            nr.WO_NBR,
            nr.WO_TYPE_DESC,
            nr.TRANSFERRED_FLG,
            nr.ACTIVITY,
            nr.TOTAL_NET_REV,
            nr.ACCT_CHANGE_CNT,
            nr.PSU_CONNECT,
            nr.PSU_DISCONNECT,
            schd.EMPLOYEE_TYPE_CD,
            schd.SALES_CHANNEL_GROUP_NM,
            schd.SALES_CHANNEL_NM,
            schd.SALES_SUB_CHANNEL_NM,
            schd.AFFILIATE_NM,
            schd.DISPLAY_CHANNEL_GROUP_NM,
            csd.SUB_STATUS_DESC,
            sdim.SITE_ID,
            sdim.SITE_DESC
        FROM
            NET_REVENUE nr
            INNER JOIN SCHD schd on nr.SALES_CHANNEL_HIER_KEY = schd.SALES_CHANNEL_HIER_KEY
            INNER JOIN CUSTOMER_SUB_STATUS csd on nr.CUSTOMER_SUBSTATUS_KEY = csd.CUSTOMER_SUBSTATUS_KEY
            INNER JOIN SITE_DIM sdim on nr.SITE_KEY = sdim.SITE_KEY
            ),
        
        COMBINED_NRPA AS (SELECT
            LAST_DAY (TIME_KEY) AS WO_Month_End,
            TIME_KEY,
            SITE_KEY,
            SITE_ID,
            SITE_DESC,
            SALES_CHANNEL_HIER_KEY,
            COX_ID_DTL_BILLING_KEY,
            COX_ID_DTL_HR_KEY,
            COX_ID_DTL_SITE_KEY,
            CS_AGENT_HIER_DLY_KEY,
            CS_AGENT_HIER_MTHLY_KEY,
            CUSTOMER_SUBSTATUS_KEY,
            SUB_STATUS_DESC,
            ACCNT_NBR,
            CUSTOMER_KEY,
            WO_NBR,
            WO_TYPE_DESC,
            TRANSFERRED_FLG,
            DISPLAY_CHANNEL_GROUP_NM,
            SALES_CHANNEL_GROUP_NM,
            SALES_CHANNEL_NM,
            SALES_SUB_CHANNEL_NM,
            AFFILIATE_NM,
            EMPLOYEE_TYPE_CD,
            CASE
                WHEN CUSTOMER_SUBSTATUS_KEY IN (8, 9) THEN 'Transfer'
                ELSE ACTIVITY
            END AS ACTIVITY,
            TOTAL_NET_REV
        FROM
            JOINED_NRPA
            WHERE
                DISPLAY_CHANNEL_GROUP_NM IN ('Online',
                         'Inbound', 'National Affiliate', 'Retention', 'Cox Owned - Retail', 'Field Sales', 'Retail Stores', 'Third Party Retail', 'Direct')
        ),    
        
        COMBINED_PSUS AS (
        SELECT
            LAST_DAY(psus.TIME_KEY) AS WO_Month_End,
            psus.time_key,
            psus.SITE_KEY,
            sdim.SITE_ID,
            sdim.SITE_DESC,
            psus.SALES_CHANNEL_HIER_KEY,
            psus.COX_ID_DTL_BILLING_KEY,
            psus.COX_ID_DTL_HR_KEY,
            psus.COX_ID_DTL_SITE_KEY,
            psus.CS_AGENT_HIER_DLY_KEY,
            psus.CS_AGENT_HIER_MTHLY_KEY,
            psus.CUSTOMER_SUBSTATUS_KEY,
            csd.SUB_STATUS_DESC,
            psus.ACCNT_NBR,
            psus.CUSTOMER_KEY,
            psus.WO_NBR,
            psus.WO_TYPE_DESC,
            psus.TRANSFERRED_FLG,
            schd.DISPLAY_CHANNEL_GROUP_NM,
            schd.SALES_CHANNEL_GROUP_NM,
            schd.SALES_CHANNEL_NM,
            schd.SALES_SUB_CHANNEL_NM,
            schd.AFFILIATE_NM,
            schd.EMPLOYEE_TYPE_CD,
            psus.PSU_CONNECT,
            psus.PSU_DISCONNECT

            -- psus.ACTIVITY,
            -- psus.TOTAL_NET_REV,
            -- psus.ACCT_CHANGE_CNT,
        FROM
            PSUS psus
            INNER JOIN SCHD schd on psus.SALES_CHANNEL_HIER_KEY = schd.SALES_CHANNEL_HIER_KEY
            INNER JOIN CUSTOMER_SUB_STATUS csd on psus.CUSTOMER_SUBSTATUS_KEY = csd.CUSTOMER_SUBSTATUS_KEY
            INNER JOIN SITE_DIM sdim on nr.SITE_KEY = sdim.SITE_KEY
            WHERE schd.DISPLAY_CHANNEL_GROUP_NM IN ('Online', 'Inbound', 'National Affiliate', 'Retention', 'Cox Owned - Retail', 'Field Sales', 'Retail Stores', 'Third Party Retail', 'Direct' )
        ),

        NRPA_JOINED_PSUS AS (
        SELECT 
        nrpa.*,
        psus.*

        FROM COMBINED_NRPA nrpa 
        INNER JOIN COMBINED_PSUS psus 
                ON nrpa.wo_month_end = psus.wo_month_end
                AND nrpa.time_key = psus.time_key
                AND nrpa.site_key = psus.site_key
                AND nrpa.sales_channel_hier_key = psus.sales_channel_hier_key
                AND nrpa.cox_id_dtl_billing_key = psus.cox_id_dtl_billing_key
                AND nrpa.cox_id_dtl_hr_key = psus.cox_id_dtl_hr_key
                AND nrpa.cox_id_dtl_site_key = psus.cox_id_dtl_site_key
                AND nrpa.cs_agent_hier_dly_key = psus.cs_agent_hier_dly_key
                AND nrpa.cs_agent_hier_mthly_key = psus.cs_agent_hier_mthly_key
                AND nrpa.customer_substatus_key = psus.customer_substatus_key
                AND nrpa.accnt_nbr = psus.accnt_nbr
                AND nrpa.customer_key = psus.customer_key
                AND nrpa.wo_nbr = psus.wo_nbr
        
        ),

        NRPA_ACCT_CHG AS (
        SELECT  
                WO_MONTH_END,
                TIME_KEY,
                SITE_KEY,
                SITE_ID,
                SITE_DESC,
                SALES_CHANNEL_HIER_KEY,
                COX_ID_DTL_BILLING_KEY,
                COX_ID_DTL_HR_KEY,
                COX_ID_DTL_SITE_KEY,
                CS_AGENT_HIER_DLY_KEY,
                CS_AGENT_HIER_MTHLY_KEY,
                CUSTOMER_SUBSTATUS_KEY,
                SUB_STATUS_DESC,
                ACCNT_NBR,
                CUSTOMER_KEY,
                WO_NBR,
                WO_TYPE_DESC,
                TRANSFERRED_FLG,
                DISPLAY_CHANNEL_GROUP_NM,
                SALES_CHANNEL_GROUP_NM,
                SALES_CHANNEL_NM,
                SALES_SUB_CHANNEL_NM,
                AFFILIATE_NM,
                EMPLOYEE_TYPE_CD,
                ACTIVITY,
                ACCT_CHANGE_CNT

        FROM (
                SELECT 
                        TIME_KEY,
                        COX_ID_DTL_BILLING_KEY,
                        COX_ID_DTL_HR_KEY,
                        COX_ID_DTL_SITE_KEY,
                        SALES_CHANNEL_HIER_KEY,
                        CS_AGENT_HIER_DLY_KEY,
                        CS_AGENT_HIER_MTHLY_KEY,
                        CUSTOMER_SUBSTATUS_KEY,
                        SITE_KEY,
                        ACCNT_NBR,
                        CUSTOMER_KEY,
                        WO_NBR,
                        WO_TYPE_DESC,
                        TRANSFERRED_FLG,
                        ACCT_CHANGE_CNT,
                        EMPLOYEE_TYPE_CD,
                        SALES_CHANNEL_GROUP_NM,
                        SALES_CHANNEL_NM,
                        SALES_SUB_CHANNEL_NM,
                        AFFILIATE_NM,
                        DISPLAY_CHANNEL_GROUP_NM,
                        SUB_STATUS_DESC,
                        SITE_ID,
                        SITE_DESC,
                        CASE 
                                WHEN CUSTOMER_SUBSTATUS_KEY NOT IN (8,9) THEN ACTIVITY
                                WHEN CUSTOMER_SUBSTATUS_KEY IN (8) THEN 'Transfer' 
                                ELSE 'Existing Transfer'
                        END AS ACTIVITY,
                        LAST_DAY(TIME_KEY) AS WO_Month_End

                FROM 
                        JOINED_NRPA
               ) 
        WHERE ACTIVITY <> 'Existing Transfer'
        AND DISPLAY_CHANNEL_GROUP_NM IN ('Online', 'Inbound', 'National Affiliate', 'Retention', 'Cox Owned - Retail', 'Field Sales', 'Retail Stores', 'Third Party Retail', 'Direct')
        
        ),

        NRPA_ACCT_CHG_ALL AS (
                SELECT 
                        TIME_KEY,
                        COX_ID_DTL_BILLING_KEY,
                        COX_ID_DTL_HR_KEY,
                        COX_ID_DTL_SITE_KEY,
                        SALES_CHANNEL_HIER_KEY,
                        CS_AGENT_HIER_DLY_KEY,
                        CS_AGENT_HIER_MTHLY_KEY,
                        CUSTOMER_SUBSTATUS_KEY,
                        SITE_KEY,
                        ACCNT_NBR,
                        CUSTOMER_KEY,
                        WO_NBR,
                        WO_TYPE_DESC,
                        TRANSFERRED_FLG,
                        ACCT_CHANGE_CNT,
                        EMPLOYEE_TYPE_CD,
                        SALES_CHANNEL_GROUP_NM,
                        SALES_CHANNEL_NM,
                        SALES_SUB_CHANNEL_NM,
                        AFFILIATE_NM,
                        DISPLAY_CHANNEL_GROUP_NM,
                        SUB_STATUS_DESC,
                        SITE_ID,
                        SITE_DESC,
                        CASE 
                                WHEN "CUSTOMER_SUBSTATUS_KEY" NOT IN (8,9) THEN "ACTIVITY"
                                WHEN "CUSTOMER_SUBSTATUS_KEY" IN (8,9) THEN 'Transfer' 
                        ELSE 'Other'
                        END,
                        LAST_DAY(TIME_KEY) AS WO_Month_End

                FROM 
                        JOINED_NRPA

        ) 

        """
        df = spark.sql(final_query)
        df.createOrReplaceTempView("NRPA")
        return df