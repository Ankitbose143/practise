# This Lambda is to provide lf permissions to databases owned by EDS Non-Prod 

########################

######################################

import json
import boto3
import sys
from datetime import datetime, timedelta
import os
from botocore.config import Config
from operator import itemgetter

session = boto3.Session()
glue = session.client('glue')
lakeformation = session.client('lakeformation')

iam_principal_de = {'DataLakePrincipalIdentifier': 'arn:aws:iam::254158912258:role/cci-svc-data-exchange-framework-role'}
iam_principal = {'DataLakePrincipalIdentifier': 'arn:aws:iam::254158912258:role/cci-svc-cpra-rtoo-role'}
iam_principal_dt = {'DataLakePrincipalIdentifier': 'arn:aws:iam::254158912258:role/cci-svc-data-transformation-framework-iceberg-role-dev'}
iam_principal_svc_glue= {'DataLakePrincipalIdentifier': 'arn:aws:iam::254158912258:role/cci-svc-glueservice'}
iam_principal_svc_dp= {'DataLakePrincipalIdentifier': 'arn:aws:iam::254158912258:role/cci-svc-dss-datapipeline'}
iam_principal_svc_dt = {'DataLakePrincipalIdentifier': 'arn:aws:iam::254158912258:role/cci-svc-data-transformation-framework-role'}
#iam_principal_svc_pf = {'DataLakePrincipalIdentifier': 'arn:aws:iam::254158912258:role/cci-svc-platform-role-test'}

iam_principal_eds_readwrite = {'DataLakePrincipalIdentifier': 'arn:aws:iam::254158912258:role/EDS_N_READWRITE'}
iam_principal_switch_dev = {'DataLakePrincipalIdentifier': 'arn:aws:iam::254158912258:role/cci-switchrole-developers'}
iam_principal_switch_dev2 = {'DataLakePrincipalIdentifier': 'arn:aws:iam::254158912258:role/cci-switchrole-developers2'}
iam_principal_switch_qa = {'DataLakePrincipalIdentifier': 'arn:aws:iam::254158912258:role/cci-switchrole-qa'}
# iam_principal_entity_res = {'DataLakePrincipalIdentifier': 'arn:aws:iam::254158912258:role/cci-svc-entity-resolution-role'}
iam_allowed_principal = {'DataLakePrincipalIdentifier': 'IAM_ALLOWED_PRINCIPALS'}


def lambda_handler(event, context):
    
    now = str(datetime.now())[:-7]
    one_hour_ago = str(datetime.now() + timedelta(hours=-1, minutes=-10))[:-7]
    
    glue_client = boto3.client("glue")
    #database_list = ['call','camp_mgmt',  'cci_base',  'cci_cust_mgmt',  'cci_fulf',  'cci_mkt_sale',  'cdm',  'chsi_usage',  'cust_care',  'cust_value',   'edgehealth',  'edw',  'equipment',  'identity', 'int_prov',  'ivr_trigger_app',  'ivrrpt',  'leadmgt',  'lmi', 'mdu',  'mobile_data', 'msadmin', 'msuser',    'npm',   'pcc',  'pega_data', 'sage_reporting',  'sales', 'survey','sync_gnis','titan','uet_rep','video','video_usage','wfm','wifi','realtime']
    database_list=['pstage']
    
    print(database_list)
    
    for db in database_list:
        print('...Granting permissions on database ' +db + '...')
        database_resource = {'Database': {'Name': db}}
        table_resource_wc = {'Table': {'DatabaseName': db,'TableWildcard' : {}}}
        
        #table_resource = {'Table': {'DatabaseName': db,'Name' : 'cust_acct_product_flags_fact'}}
        print(database_resource)
        # Granting Permissions to database.
        lakeformation.grant_permissions(Principal=iam_principal, Resource=database_resource,Permissions=['ALL'],PermissionsWithGrantOption=[])
        lakeformation.grant_permissions(Principal=iam_principal_dt, Resource=database_resource,Permissions=['ALL'],PermissionsWithGrantOption=[])
        lakeformation.grant_permissions(Principal=iam_principal_de, Resource=database_resource,Permissions=['ALL'],PermissionsWithGrantOption=[])
        lakeformation.grant_permissions(Principal=iam_principal_svc_glue, Resource=database_resource,Permissions=['ALL'],PermissionsWithGrantOption=[])
        lakeformation.grant_permissions(Principal=iam_principal_svc_dp, Resource=database_resource,Permissions=['ALL'],PermissionsWithGrantOption=[])
        lakeformation.grant_permissions(Principal=iam_principal_svc_dt, Resource=database_resource,Permissions=['ALL'],PermissionsWithGrantOption=[])
        #lakeformation.grant_permissions(Principal=iam_principal_svc_pf, Resource=database_resource,Permissions=['ALL'],PermissionsWithGrantOption=[]) # platform role
        lakeformation.grant_permissions(Principal=iam_principal_switch_qa, Resource=database_resource,Permissions=['ALL'],PermissionsWithGrantOption=[])
        
        
        lakeformation.grant_permissions(Principal=iam_principal_eds_readwrite, Resource=database_resource,Permissions=['ALL'],PermissionsWithGrantOption=['ALL'])
        # lakeformation.grant_permissions(Principal=iam_principal_entity_res, Resource=database_resource,Permissions=['ALL'],PermissionsWithGrantOption=['ALL'])
        
        # Granting Permissions to all tables.
        lakeformation.grant_permissions(Principal=iam_principal, Resource=table_resource_wc,Permissions=['SELECT','DESCRIBE'],PermissionsWithGrantOption=[])
        lakeformation.grant_permissions(Principal=iam_principal_eds_readwrite, Resource=table_resource_wc,Permissions=['ALL'],PermissionsWithGrantOption=[])
        lakeformation.grant_permissions(Principal=iam_principal_switch_dev, Resource=table_resource_wc,Permissions=['SELECT','DESCRIBE', 'ALTER', 'INSERT'],PermissionsWithGrantOption=[])
        lakeformation.grant_permissions(Principal=iam_principal_switch_dev2, Resource=table_resource_wc,Permissions=['SELECT','DESCRIBE', 'ALTER', 'INSERT'],PermissionsWithGrantOption=[])
        lakeformation.grant_permissions(Principal=iam_principal_switch_qa, Resource=table_resource_wc,Permissions=['ALL'],PermissionsWithGrantOption=[])
        lakeformation.grant_permissions(Principal=iam_principal_svc_dp, Resource=table_resource_wc,Permissions=['ALL'],PermissionsWithGrantOption=[])
        lakeformation.grant_permissions(Principal=iam_principal_svc_glue, Resource=table_resource_wc,Permissions=['ALL'],PermissionsWithGrantOption=[])
        lakeformation.grant_permissions(Principal=iam_principal_de, Resource=database_resource,Permissions=['ALL'],PermissionsWithGrantOption=[])
        lakeformation.grant_permissions(Principal=iam_principal_dt, Resource=database_resource,Permissions=['ALL'],PermissionsWithGrantOption=[])
        lakeformation.grant_permissions(Principal=iam_principal_svc_dt, Resource=table_resource_wc,Permissions=['ALL'],PermissionsWithGrantOption=[])
        #lakeformation.grant_permissions(Principal=iam_principal_svc_pf, Resource=table_resource_wc,Permissions=['ALL'],PermissionsWithGrantOption=['']) # platform role
        # Revoking IAM_ALLOWED_PRINCIPALS from each table to make them visible in other accounts
        
        tables_list = []
        next_token = None
        
        # Pagination logic to fetch more than 100 tables
        while True:
            params = {'DatabaseName': db, 'MaxResults': 100}
            if next_token:
                params['NextToken'] = next_token
                
            response = glue_client.get_tables(**params)
            tables_list.extend(response['TableList'])
            
            if 'NextToken' not in response:
                break
                
            next_token = response['NextToken']
            
        #tables_list =  glue_client.get_tables(DatabaseName=db)['TableList']
        
        athena_tables = list(map(itemgetter('Name'), tables_list))
        print ( "Removing iam allowed principal from individual table in the database " + db)
        num_tables=0
        for gluetable in athena_tables:
            num_tables=num_tables+1
            tablename=gluetable
            print ( "Removing iam allowed principal from individual table in the database " + db + '.'+tablename)
            table_resource = {'Table': {'DatabaseName': db,'Name' : tablename}}
            try:
                lakeformation.revoke_permissions(Principal=iam_allowed_principal,Resource=table_resource,Permissions=['ALL'],PermissionsWithGrantOption=[])
                # lakeformation.revoke_permissions(Principal=iam_allowed_principal,Resource=table_resource,Permissions=[],PermissionsWithGrantOption=[])
            except Exception as err:
                print("Cannot execute query")
                description = "Query error: {0}".format(err)
                print(description)
            print ( "Removed iam allowed principal from individual table in the database " + db + '.'+tablename)
        print(f"table count in {db} db {num_tables}")