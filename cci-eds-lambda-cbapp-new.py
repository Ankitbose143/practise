# *********************** DEV NOTE *************************************************************************************
# AUTHOR: ANKIT BOSE
# VERSION: 1
# BUILD DATE: 08/11/2023
# PROCESS NAME: CCI_EDS_LAMBDA_CBAPP
# FUNCTIONALITY: THIS LAMBDA IS FOR CBAPP and MAP/LOOKUP DATA WITH VALUES AND PUSH TO V2
# DO NOT EDIT OR TINKER!!!!!
# INVOCATIONS : V2  TRIGGERED
# **********************************************************************************************************************


import boto3
from datetime import datetime
import json
import logging
import os
import pymysql
import re
import sys
import io
# from snowflake.connector import DictCursor as Dt
import uuid
import gzip
import zipfile
import tarfile
import pandas as pd
import tempfile

global cursor
global app_nm
global domain_nm
global cif_id
global global_database_name
global rds_cur
global rds_conn
global job_run_id
global logger
global rds_file_log
global df_column_header
global browser
global browser_type
global color_depth
global resolution
global referrer_type
global plugins
global operating_systems
global languages
global javascript_version
global event
global connection_type
global country
global search_engines, file_defination_nm


global dict_browser
global dict_browser_type
global dict_color_depth
global dict_resolution
global dict_referrer_type
global dict_plugins
global dict_operating_systems
global dict_languages
global dict_javascript_version
global dict_event
global dict_connection_type
global dict_country
global dict_search_engines
global list_lookup
list_lookup = []

# IN_PROGRESS = "IN PROGRESS"
# FAILED = "FAILED"



def get_logger():
    """
    This function is used to create a logger object.
    """

    try:
        # Declaring standard format variables
        logging_format = "%(asctime)s %(levelname)s %(name)s:\t%(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"

        # Setting configuration ar per our need
        logging.basicConfig(format=logging_format, datefmt=date_format)
        temp_logger = logging.getLogger("CCI_EDS_LAMBDA_CBAPP")
        temp_logger.setLevel(logging.INFO)

        return temp_logger

    except Exception as e:
        logger.exception(
            f"Error encountered in get_logger function.\nError: {str(e)}"
        )
        print(f"Error encountered in get_logger function.\nError: {str(e)}")
        sys.exit()
        
def dict_files(data, files):
    """
    Function to read dataframe and convert to dict
    :param : search_engines_file
    :return: dictionary dict_search_engines
    """
    try:
        df = data
        print("inside dict files",df.head(2))
        selected_columns = df.iloc[:, [0, 1]]
        file_nm = dict(zip(selected_columns.iloc[:, 0], selected_columns.iloc[:, 1]))
        # print("file_nm-----------", file_nm)
        return file_nm
    except Exception as e:
        logger.error(
            f"Error encountered in dict_files function.\nError: {str(e)}"
        )
        print(f"Error encountered in get_logger function.\nError: {str(e)}")


def get_secret_string(secret_name):
    """
    This function is used to fetch sensitive information stored in Secrets Manager.
    :param secret_name: Name of the secret for which the details from Secrets Manager needs to be fetched.
    :return: Python Dictionary containing all information retrieved from Secrets Manager.
    """

    try:
        # Logging process start
        logger.info(
            "Inside get_secret_string function. Process started to fetch secrets details."
        )

        # Creating connection with Secret Manager to fetch details
        secret_manager_client = boto3.client("secretsmanager")

        # Retrieving values
        get_secret_value_response = secret_manager_client.get_secret_value(
            SecretId=secret_name
        )
        secret = eval(get_secret_value_response["SecretString"])

        logger.info(
            "Inside get_secret_string function. Process completed to fetch secrets details."
        )
        return secret

    except Exception as e:
        logger.error(
            f"Error encountered in get_secret_string function.\nError: {e}"
        )
        sys.exit()


def get_job_id():
    try:
        return str(f"{uuid.uuid4()}_{datetime.now().strftime('%Y%m%d%H%M%S')}")

    except Exception as e:
        logger.info(f"Error encountered in get_job_id function.\nError: {str(e)}")
        sys.exit()


def make_rds_connection(secret_name):
    """
    This function is used to establish connection with RDS.
    :param secret_name: Name of the RDS Secret.
    :return: Connection object with RDS, along with cursor to execute SQL queries.
    """

    # Trying 3 times to connect to RDS
    # We fetch instance information from Secrets Manager
    logger.info(
        "Inside make_rds_connection function. Process started to establish connection with RDS."
    )

    for i in range(1, 4):
        try:
            logger.info(f"Retry count: {i}")
            secret = get_secret_string(secret_name)

            # Making connection
            rds_conn = pymysql.connect(
                host=secret["host"],
                user=secret["username"],
                passwd=secret["password"],
                port=int(secret["port"]),
                db=secret["dbname"],
                autocommit=True,
            )

            rds_cur = rds_conn.cursor()
            print("rds_cur", rds_cur)
            logger.info(
                "Inside make_rds_connection function. Process completed to establish connection with RDS."
            )
            return rds_conn, rds_cur

        except Exception as e:
            i = i + 1
            if i == 3:
                logger.error(
                    f"Error encountered in make_rds_connection function.\nError: {e}"
                )
                sys.exit()
                
def frame_file_path(folder_list, file_name=""):
    """
    Function to frame the folder path from folder list along with file name
    :param folder_list:
    :param file_name:
    :return:
    """

    def check_backslash(folder_name):
        return folder_name + "/" if not folder_name[-1] == "/" else folder_name

    try:
        if "" in folder_list:
           folder_list = list(filter(None, folder_list))
           folder_list.append("")
        folder_names = [check_backslash(name) if str(name).strip() != '' else "/" for name in folder_list ]
        if len(folder_names) > 1 and folder_names[-1] == '/':
            del folder_names[-1]
        folder_path = "".join(folder_names)
        if folder_path != "/":
           folder_path = folder_path[1:] if folder_path[0] == "/" else folder_path
        file_path = str(folder_path + file_name) if file_name != "" else ""
    except Exception as exception:
        print("Function Name: {} Error: {}".format(frame_file_path.__name__, str(exception)))
        logger.error("Function Name: {} Error: {}".format("frame_file_path", str(exception)))
        raise Exception(str(exception))
    return folder_path, file_path
    
def list_s3_objects(bucket, prefix, s3_client):
    """
    Function to list all object from specific bucket location
    :param s3_client:
    :param bucket:
    :param prefix:
    :return:
    """
    try:
        file_names = []
        full_file_paths = []
        bucket_details = {'Bucket': bucket, 'Prefix': prefix}
        print("bucket_details", bucket_details)
        
        while True:
            response = s3_client.list_objects_v2(**bucket_details)
            print("response", response)
            if 'Contents' in response.keys():
                for obj in response['Contents']:
                    key = obj['Key'].split('/')[-1]
                    if key:
                        file_names.append(key)
                        full_file_paths.append(obj['Key'])
                    else:
                        pass
            try:
                bucket_details['ContinuationToken'] = response['NextContinuationToken']
            except KeyError:
                break
        print("file_names---",file_names, full_file_paths)
        return file_names, full_file_paths
    except Exception as exception:
        print("exception", exception)
        logger.error("Error in Function Name: {} Error: {}".format("list_s3_objects", str(exception)))
        raise Exception(str(exception))    

# takes 37 seconds to unzip file
def unzip_file(rds_cur, file_names, full_file_paths, file_defination_dict, job_id_list):
    try:
        print("inside zip")
        s3_client = boto3.client('s3')
        v2_framework_dict = json.loads(os.environ['v2_framework'])
        target_bucket = v2_framework_dict['target_bucket']
        v2_curated_bucket =  v2_framework_dict['curated_bucket']
        key_out_path = v2_framework_dict['key_out_path']
        stage_bucket = v2_framework_dict['stage_bucket']
        bucket = v2_framework_dict['stage_bucket']
        file_path = v2_framework_dict['file_path']
        unzip_path3 = v2_framework_dict['unzip_path3']
        unzip_path = v2_framework_dict['unzip_path']
        file_name_pattern = ''
        print("file_names: ", file_names)
        match_dates_list = []
        for dates_chk in file_names:
            if not dates_chk.endswith('.tar.gz'):
                match_date = re.search(r'\d{4}-\d{2}-\d{2}', dates_chk)
                print("match---match_dates", match_date)
                if not match_date is None:
                    match_dates = match_date.group()
                    print("match---match_dates111", match_dates)
                    match_dates_list.append(match_dates)
                    print("match---match_dates_list", match_dates_list)
            
        print("file_path: ", full_file_paths)
        file_names_paths = list(zip(file_names, full_file_paths))
        print("file_names_paths-->=>",file_names_paths)
        print("file_defination_dict-->=>",file_defination_dict)
        print("job_id_list-->=>",job_id_list)
        
        global df_column_header
        flag = 0
        Key_file_list = []
        data_file = {}
        for name, key in file_names_paths:
            print("name, key-->", name, key)
            
            file_extension = os.path.splitext(name)[1][1:]
            file_extension2 = file_extension
            print("file_extn", file_extension)
            if '.tar' in name:
                file_extension1 = os.path.splitext(name)
                print("file_extna", file_extension1)
                file_extension2 = os.path.splitext(file_extension1[0])[1][1:]
                print("file_ext1n", file_extension2)
            if 'column_headers.tsv' in name:
                try:
                    print("files col",name, key)
                    # existing_buffer_header = io.BytesIO()
                    # s3_client.download_fileobj(bucket, key, existing_buffer_header)
                    existing_buffer_header = io.BytesIO(s3_client.get_object(Bucket=bucket, Key=key)['Body'].read())
                    
                    df_column_head = pd.read_csv(existing_buffer_header, sep = '\t',encoding='ISO-8859-1')
                    df_column_header = list(df_column_head.columns)
                    # print("files df_column_head",df_column_header)
                    # df_column_head = pd.read_csv(archive.extractfile(files), sep ='\t')
                except Exception as e:
                    print("error reading column header at start", str(e))
            if file_extension2 == 'tar':
                try:
                    # update_file_log(rds_cur, "STARTED", "TAR EXTRACTION STARTED", "TAR EXTRACTION ", file_defination_nm)
                    print("b ucket, key111", bucket, key)
                    buffered = io.BytesIO(s3_client.get_object(Bucket=bucket, Key=key)['Body'].read())
    
                    archive = tarfile.open(fileobj=buffered)
                    print("archive",archive.getnames())
                    for files in archive.getnames():
                        print("bucketname, key", name, key, files)
                        df_counters = {}
                        # buffered = io.BytesIO(s3_client.get_object(Bucket=bucket, Key=key)['Body'].read())
                        s3_client.upload_fileobj(archive.extractfile(files), Bucket=stage_bucket,
                                                     Key=unzip_path3+files)
                        print("tempc_done",files)
                        # update_file_log(rds_cur, "STARTED", "TAR EXTRACTION COMPLETED", "TAR EXTRACTION COMPLETED", file_defination_nm)
                        if 'column_headers.tsv' in files:
                            print("files col123",files)
                            
                            df_column_head = pd.read_csv(archive.extractfile(files), sep ='\t',encoding='ISO-8859-1')
                            jobid = job_id_list.get(files)
                            print("jobid column header", jobid)
                        
                            if not jobid or jobid is None:
                                jobid = get_job_id()
                                job_id = insert_file_log(rds_cur,files, jobid)
                                job_id_list[files]= jobid
                                # job_id = insert_file_log(rds_cur,fnm, job_run_id)
                                print("job_run_id1231", jobid, job_id_list)
                                table_nm = files
                                if '.tsv' in files:
                                    table_nm = files.replace('.tsv', '')
                                print("table name column", table_nm)
                                cif_id = insert_cif_job_status_record(rds_cur, files, table_nm)
                                file_defination_dict[files] = cif_id
                            else:
                                cif_id = file_defination_dict.get(files)
                                table_nm = files
                                if '.tsv' in files:
                                    table_nm = files.replace('.tsv', '')
                                if cif_id is None:
                                    cif_id = insert_cif_job_status_record(rds_cur, files, table_nm)
                                    file_defination_dict[files] = cif_id
                                    
                            print("cifid--->", cif_id)
                            
                            print(job_id_list)
                            df_column_header = list(df_column_head.columns)
                            print("jobid222", jobid)
                            # update_file_log(rds_cur, "COMPLETED", "COMPLETED", "COLUMN HEADER PROCESSED", files, jobid)
                            
                            update_cif_job_status_record(rds_cur,cif_id, len(df_column_header), '', files, 'N')
                            # print("df_column_header123",list(df_column_head.columns))
                            update_file_log(rds_cur, "STARTED", "COLUMN ADDING STARTED", "COLUMN ADDITION IN DATAFRAME", files, jobid)
                            print("Key_file_list123--", Key_file_list)
                            if Key_file_list:
                                Key_file_list = list(set(Key_file_list))
                                for key_fl in Key_file_list:
                                    key_fl_chk = key_fl.replace(unzip_path3,'')
                                    
                                    jobid = job_id_list.get(key_fl_chk)
                                    print("jobid---file", jobid, key_fl)
                                    # if Key_file:
                                    print("key file present",key_fl, jobid)
                                    data_header_mapping(key_fl, jobid)
                            else:
                                print("no key file present")
                        else:
                            print("else not column headers",files)
                            Key_file_list = list(set(Key_file_list))
                            # Key_file_list.append(files)
                            # update_file_log(rds_cur, "IN PROGRESS", "DICT DATAFRAME STARTED "+files, "DICT CREATION IN DATAFRAME "+files, file_defination_nm)
                            jobid = job_id_list.get(files)
                            print("jobid---file---", jobid, files)
                            if not jobid or jobid is None:
                                jobid = get_job_id()
                                job_id = insert_file_log(rds_cur,files, jobid)
                                job_id_list[files]= jobid
                                # job_id = insert_file_log(rds_cur,fnm, job_run_id)
                                print("job_run_id123", jobid, job_id_list)
                                table_nm = files
                                if '.tsv' in files:
                                    table_nm = files.replace('.tsv', '')
                                print("table name", table_nm)
                                cif_id = insert_cif_job_status_record(rds_cur, files, table_nm)
                                file_defination_dict[files] = cif_id
                            else:
                                cif_id = file_defination_dict.get(files)
                                table_nm = files
                                if '.tsv' in files:
                                    table_nm = files.replace('.tsv', '')
                                if cif_id is None:
                                    cif_id = insert_cif_job_status_record(rds_cur, files, table_nm)
                                    file_defination_dict[files] = cif_id
                        
                            
                            # print("len file", files, len(df_file_check))
                            df_count, data_file = dict_dataframe(files, archive, jobid)
                            
                            # update_cif_job_status_record(rds_cur,cif_id, df_count, '', files, 'N')
                            file_dict_files = files.replace('.tsv', '')
                            print("file_dict_files", file_dict_files)
                            print("file_defination_dict",file_defination_dict)
                            print("cif id 123", cif_id)
                            df_counters['FULL'] = df_count
                            # df_counter[dt] = df_count
                            
                            
                            update_cif_job_status_record(rds_cur,cif_id, df_count, '', files, 'N')
                            if match_dates_list:
                                for date_chk in match_dates_list:
                                    df_counters[date_chk] = df_count
                                    initiate_v2_process(df_counters,cif_id, 'full', '', file_dict_files)
                            else:
                                # current_date = datetime.now().date()
                                formatted_date = datetime.now().strftime("%Y-%m-%d")
                                df_counters[formatted_date] = df_count
                                initiate_v2_process(df_counters,cif_id, 'full', '', file_dict_files)
                            flag = 1
                    archive.close()
                    if 'cbapp/' in key:
                        print("fls cbapp", key)
                        fls = key.replace('cbapp/', '')
                        print('fls')
                        cif_id = file_defination_dict.get(fls)
                        jobid = job_id_list.get(fls)
                        update_file_log(rds_cur, "COMPLETED", "COMPLETED", "COLUMN HEADER PROCESSED", fls, jobid)
                        update_cif_job_status_record(rds_cur,cif_id, 0, '', fls, 'N')
                        
                except Exception as exception:
                    print("Error tar file tar",exception)
                    sys.exit(1)
            elif file_extension == 'gz':
                try:
                    # update_file_log(rds_cur, "IN PROGRESS", "GZ EXTRACTION STARTED", "GZ EXTRACTION", file_defination_nm)
                    print("name gz file", name)
                    print("file_defination_dict.items()", file_defination_dict.items())
                    for file_checks, vl in file_defination_dict.items():
                        print("file_checks123", file_checks, vl)
                        if file_checks in name:
                            buffer = io.BytesIO(s3_client.get_object(Bucket=bucket, Key=key)['Body'].read())
                            print("buffer", buffer)
                            z = gzip.GzipFile(fileobj=buffer)
                            print("z123", z, name.replace(".gz", ""))
                            print("frame_file_path([unzip_path]",frame_file_path([unzip_path], name.replace(".gz", "")))
                            Key_file=frame_file_path([unzip_path], name.replace(".gz", ""))[1]
                            s3_client.upload_fileobj(Fileobj=z, Bucket=stage_bucket,
                                                     Key=frame_file_path([unzip_path], name.replace(".gz", ""))[1])
                            Key_file_list = list(set(Key_file_list))
                            Key_file_list.append(Key_file)
                            print("Key_file_list143--", Key_file_list)
                except Exception as exception:
                    print("Error gz file gz",str(exception))
                    sys.exit(1)
            elif file_extension == 'zip':
                try:
                    print("name zip file", name)
                    buffer = io.BytesIO(s3_client.get_object(Bucket=bucket, Key=key)['Body'].read())
                    z = zipfile.ZipFile(buffer)
                    for filename in z.namelist():
                        file_info = z.getinfo(filename)
                        s3_client.upload_fileobj(Fileobj=z.open(filename), Bucket=stage_bucket,
                                                 Key=frame_file_path([unzip_path], filename)[1])
                    # update_file_log_status(name, "IN PROGRESS", "")
                except Exception as exception:
                    print("Error zip file zip",exception)
                    sys.exit(1)
            elif file_extension == '.tsv' or file_extension == 'tsv':
                try:
                    print("name ctsv file", name, key)
                    for file_checks, _ in file_defination_dict.items():
                        # print("file_checks", file_checks)
                        if file_checks not in name:
                            if flag != 1:
                                # update_file_log(rds_cur, "IN PROGRESS", "TSV FILE DICT MAPPING STARTED", "TSV FILE", file_defination_nm)
                                print("dat_file ----123>", file_defination_nm)
                                # buffered = io.BytesIO(s3_client.get_object(Bucket=bucket, Key=key)['Body'].read())
                    
                                # archive = tarfile.open(fileobj=buffered)
                                # jobid = job_id_list.get(files)
                                # print("jobid---file", jobid)
                                # df_count, data_file =dict_dataframe(files, archive,jobid)
                                # df_counters['FULL'] = df_count
                                flag = 1
                                print("dat_file ---->", data_file)
                            else:
                                print("file name", key)
                except Exception as exception:
                    print("Error TSV FILE DICT MAPPING",exception)
                    sys.exit(1)
            elif file_extension == '.txt' or file_extension == 'txt':
                try:
                    print("name zip132", name)
                    cif_id = file_defination_dict.get(name)
                    update_cif_job_status_record(rds_cur,cif_id, 0, '', name, 'N')
                    print("job_id_list, name3", name, job_id_list)
                    jobid = job_id_list.get(name)
                    update_file_log(rds_cur, "COMPLETED", "COMPLETED", "COLUMN HEADER PROCESSED", name, jobid)
                    logger.info('File txt type missing or incorrectly specified. Review metadata information.')
                except Exception as exception:
                    print("Error TXT FILE ",exception)
                    sys.exit(1)
            else:
                print("name zip", name)
                cif_id = file_defination_dict.get(name)
                update_cif_job_status_record(rds_cur,cif_id, 0, '', name, 'N')
                print("job_id_list, name", name, job_id_list)
                jobid = job_id_list.get(name)
                update_file_log(rds_cur, "COMPLETED", "COMPLETED", "COLUMN HEADER PROCESSED", name, jobid)
                logger.info('File zip type missing or incorrectly specified. Review metadata information.')
        # raise Exception("check")
        print("Key_file_list1111", Key_file_list, flag)
        Key_file_list = list(set(Key_file_list))
        # print("data_file", data_file)
        df_counter = {}
        if flag ==1 and Key_file_list:
            try:
                print("inside data mapping", Key_file_list)
                for key_fl in Key_file_list:
                    key_fl_chk = key_fl.replace(unzip_path3,'')
                    match = re.search(r'\d{4}-\d{2}-\d{2}', key_fl_chk)
                    match_g = match.group()
                    print("match---", match_g)
                    cif_id = file_defination_dict.get(key_fl_chk)
                    jobid = job_id_list.get(key_fl_chk)
                    print("file found in dict cid is : ", cif_id)
                    print("file found in jobid is : ", jobid, key_fl)
                    dt = match_g
                    # df_count = len(df)
                    # existing_buffer = io.BytesIO()
                    print("df_column_header",df_column_header)
                    print("key---", key_fl)
                    existing_buffer = io.BytesIO(s3_client.get_object(Bucket=bucket, Key=key_fl)['Body'].read())
                    # s3_client.download_fileobj(bucket, key_fl, existing_buffer)
                    existing_data = pd.read_csv(existing_buffer, sep = '\t', header=None,encoding='ISO-8859-1')
                    out_buffer = io.BytesIO()
                    # existing_data = existing_data.reset_index(drop=True, inplace=True)
                    existing_data.columns = df_column_header
                    print("existing_data.columns",existing_data.columns)
                    # existing_data['geo_zip'] = pd.to_numeric(existing_data['geo_zip'], errors='coerce').astype('Int64')
                    df_count= len(existing_data)
                    print("existing data head", existing_data.head(2))
                    print("df_count--", key_fl_chk, df_count)
                    # out_buffer = io.BytesIO()
                    # # df['browser']= df['browser'].astype(str)
                    # existing_data['browser']= pd.to_numeric(existing_data['browser'], errors='coerce').astype('Int64')
                    # existing_data['browser_height'] = pd.to_numeric(existing_data['browser_height'], errors='coerce').astype('Int64')
                    # existing_data['browser_width'] = pd.to_numeric(existing_data['browser_width'], errors='coerce').astype('Int64')
                    # existing_data['click_action_type'] = pd.to_numeric(existing_data['click_action_type'], errors='coerce').astype('Int64')
                    # existing_data['click_context_type'] = pd.to_numeric(existing_data['click_context_type'], errors='coerce').astype('Int64')
                    # existing_data['click_sourceid'] = pd.to_numeric(existing_data['click_sourceid'], errors='coerce').astype('Int64')
                    columns_to_convert  = ['browser', 'browser_height', 'browser_width', 'click_action_type', 'click_context_type', 'click_sourceid', 'color', 'connection_type', 'country', 'curr_factor', 'curr_rate', 'cust_hit_time_gmt', 'daily_visitor', 'duplicate_purchase', 'exclude_hit', 'first_hit_ref_type', 'first_hit_time_gmt', 'geo_dma', 'geo_zip', 'hit_source', 'hit_time_gmt', 'hitid_high', 'hitid_low', 'hourly_visitor', 'javascript', 'language', 'last_hit_time_gmt', 'last_purchase_num', 'last_purchase_time_gmt', 'mcvisid', 'mobile_id', 'monthly_visitor', 'new_visit', 'os', 'page_event', 'paid_search', 'post_browser_height', 'post_browser_width', 'post_cust_hit_time_gmt', 'post_evar7', 'post_evar13', 'post_mobiledayofweek', 'post_mobiledayssincefirstuse', 'post_mobiledayssincelastuse', 'post_mobilehourofday', 'post_mobilelaunchnumber', 'post_page_event', 'post_prop26', 'post_prop52', 'post_search_engine', 'post_visid_high', 'post_visid_low', 'post_visid_type', 'prev_page', 'quarterly_visitor', 'ref_type', 'resolution', 'search_engine', 'search_page_num', 'secondary_hit', 'sourceid', 'user_hash', 'userid', 'va_closer_id', 'va_finder_id', 'va_instance_event', 'va_new_engagement', 'visid_high', 'visid_low', 'visid_timestamp', 'visid_type', 'visit_num', 'visit_page_num', 'visit_ref_type', 'visit_search_engine', 'visit_start_time_gmt', 'weekly_visitor', 'yearly_visitor']
                    for column in columns_to_convert:
                        existing_data[column] = pd.to_numeric(existing_data[column], errors='coerce')
    
                        # Step 2: Handle NaN values (replace with 0, but adjust as needed)
                        existing_data[column] = existing_data[column].fillna(0)
                    
                        # Step 3: Convert to integers
                        existing_data[column] = existing_data[column].astype(int)
                    columns_to_convert_str = ['post_prop12']
                    for columnstr in columns_to_convert_str:
                        existing_data[columnstr] = existing_data[columnstr].astype(str)
                            # existing_data[columnstr] = pd.to_numeric(existing_data[columnstr], errors='coerce')
        
                            # Step 2: Handle NaN values (replace with 0, but adjust as needed)
                            # existing_data[columnstr] = existing_data[columnstr].fillna(0)
                        
                            # Step 3: Convert to integers
                        # existing_data[column] = pd.to_numeric(existing_data[column], errors='coerce').astype('Int64')
                        # existing_data[column] = existing_data[column].astype(bytes)
                    # existing_data['c_color']= pd.to_numeric(existing_data['c_color'], errors='coerce').astype('Int64')
                    # df['resolution']= df['resolution'].astype(str)
                    # df['first_hit_ref_type']= df['first_hit_ref_type'].astype(str)
                    # existing_data['plugins']= pd.to_numeric(existing_data['plugins'], errors='coerce').astype('Int64')
                    # df['os']= df['os'].astype(str)
                    # df['language']= df['language'].astype(str)
                    # df['javascript']= df['javascript'].astype(str)
                    # existing_data['event_list']= pd.to_numeric(existing_data['event_list'], errors='coerce').astype('Int64')
                    # df['connection_type']= df['connection_type'].astype(str)
                    # df['country']= df['country'].astype(str)
                    # df['search_engine']= df['search_engine'].astype('Int64')
                    # existing_data['geo_zip'] = pd.to_numeric(existing_data['geo_zip'], errors='coerce').astype('Int64')
                    # df['mobile_id'] = pd.to_numeric(df['mobile_id'], errors='coerce').astype('Int64')
                    # df['browser_height'] = pd.to_numeric(df['browser_height'], errors='coerce').astype('Int64')
                    print("print---existing_data.dtypes before)", existing_data.dtypes)
                    # for column in existing_data.columns:
                        # existing_data[column] = existing_data[column].astype(bytes)
                    existing_data.columns = df_column_header
                    print("print---existing_data.dtypes before 999)", existing_data.head(2), len(existing_data))
                    print("df.iloc",list(existing_data.iloc[0]))
                    mask = ~existing_data.apply(lambda row: 'adclassificationcreative' in row.values or 'adload' in row.values, axis=1)
                    print("mask", mask)
                    # Apply the mask to keep only rows that meet the condition
                    existing_data = existing_data[mask]
                    
                    # Reset index after filtering
                    existing_data = existing_data.reset_index(drop=True)
                    # for i in range(10):
                    #     print("list(existing_data.iloc[i])", list(existing_data.iloc[i]), i)
                    #     print("list(existing_data.iloc[i]) ad", 'adclassificationcreative' in list(existing_data.iloc[i]), i)
                    #     print("list(existing_data.iloc[i]) adload", 'adload' in list(existing_data.iloc[i]), i)
                    #     if 'adclassificationcreative' in list(existing_data.iloc[i]) or 'adload' in list(existing_data.iloc[i]):
                    #         # Drop the first row (index 0) which is now redundant
                    #         print("dropped first row", i)
                    #         existing_data = existing_data.drop(i)
                    #     print("print---existing_data.dtypes before 999)222", existing_data.head(2), len(existing_data))
                    # print("print---existing_data.dtypes before 99911)", existing_data.head(2), len(existing_data))
                    # existing_data = existing_data.reset_index(drop=True)
                    
                    
                    print("print---existing_data.dtypes after999)", existing_data.head(2), len(existing_data))
                    
                    existing_data.to_parquet(out_buffer, index=False)
                    out_buffer.seek(0)
                    # print("out s3", v2_curated_bucket)
                    key_fl_chk1 = key_fl_chk.replace('.tsv', '.parquet')
                    # existing_data.to_parquet(key_fl_chk1, index=False)
                    print("key_fl_chk1----333",key_fl_chk1)
                    key_out = key_out_path+'DT_FILE_DT='+match_g+'/'+key_fl_chk1
                    
                    s3_client.put_object(Bucket=v2_curated_bucket, Key=key_out, Body=out_buffer.getvalue())
                    
                    print("df_count111",key_fl_chk, dt, df_count, jobid)
                    df_counter[dt] = df_count
                    
                    
                    update_file_log(rds_cur, "COMPLETED", "COMPLETED", "FILE PROCESSED", key_fl_chk, jobid)
                update_cif_job_status_record(rds_cur, cif_id, df_count, '', key_fl_chk, 'N')
                print("outside data mapping df_counter", df_counter)
                initiate_v2_process(df_counter,cif_id, 'partitioned', 'FILE_DT', 'cbapp_base')
                update_cif_job_status_record(rds_cur,cif_id, df_count, '', key_fl_chk, 'N')
                return "COMPLETED", file_defination_nm,  file_defination_dict
            except Exception as exception:
                update_file_log(rds_cur, "FAILED", "FAILED"+str(exception), "FILE PROCESSED", key_fl_chk, jobid)
                print("Error unzip files",str(exception))
                print("Error unzip files file_defination_nm",file_defination_nm, jobid)
                return "FAILED", file_defination_nm,  file_defination_dict
        return "No task", file_defination_nm, file_defination_dict
    except Exception as exception:
        print("Error unzip files",str(exception))
        print("Error unzip files file_defination_nm",file_defination_nm, jobid)
        # update_file_log(rds_cur, "COMPLETED", "COMPLETED", "FILE PROCESSED", key_fl_chk, jobid)
        update_file_log(rds_cur, "FAILED", "UNZIP FAILED", "ZIP EXTRACTION FAILED"+str(exception), file_defination_nm, jobid)
        logger.error("Function Name: {} Error: {}".format("unzip_file", str(exception)))
        # rds_conn.close()
        return "FAILED "+str(exception), file_defination_nm, file_defination_dict
        
def data_header_mapping(key, jobid):
    try:
        print("data_header_mapping ")
        s3_client = boto3.client('s3')
        v2_framework_dict = json.loads(os.environ['v2_framework'])
        
        unzip_path3 = v2_framework_dict['unzip_path3']
        fname = key.replace(unzip_path3,'')
        update_file_log(rds_cur, "IN PROGRESS", "DATA HEADER MAPPING STARTED", "COLUMN HEADER IN DATAFRAME", fname, jobid)
        
        stage_bucket = v2_framework_dict['stage_bucket']
        bucket = v2_framework_dict['stage_bucket']
        file_path = v2_framework_dict['file_path']
        existing_buffer = io.BytesIO()
        # print("df_column_header",df_column_header)
        print("key---123 header", key)
        s3_client.download_fileobj(bucket, key, existing_buffer)
        existing_buffer.seek(0)
        existing_data = pd.read_csv(existing_buffer, sep = '\t', header=None,encoding='ISO-8859-1')
        print("len before column", len(existing_data))
        existing_data.columns = df_column_header
        print("len df column", len(df_column_header))
        existing_data['c_color']= pd.to_numeric(existing_data['c_color'], errors='coerce').astype('Int64')
        existing_data['plugins']= pd.to_numeric(existing_data['plugins'], errors='coerce').astype('Int64')
        existing_data['event_list']= pd.to_numeric(existing_data['event_list'], errors='coerce').astype('Int64')
        print("len before column after", len(existing_data))
        out_buffer = io.BytesIO()
        existing_data.to_csv(out_buffer, index=False, sep = '\t',encoding='ISO-8859-1')
        out_buffer.seek(0)
        s3_client.put_object(Bucket=bucket, Key=key, Body=out_buffer.getvalue())
        update_file_log(rds_cur, "COMPLETED", "DATA HEADER MAPPING COMPLETED", "COLUMN HEADER IN DATAFRAME", fname, jobid)
        return existing_data
        
    except Exception as e:
        print("Error data_header_mapping",str(e))
        # rds_conn.close()
        update_file_log(rds_cur, "FAILED", "DATA HEADER MAPPING FAILED", "COLUMN HEADER IN DATAFRAME"+str(e), fname, jobid)
        logger.error("Function Name: {} Error: {}".format("data_header_mapping", str(e)))
        sys.exit(1)
        
def data_mapping(data_file, key, key_fl_chk, match,cif_id, jobid):
    try:
        print("data mapping")
        s3_client = boto3.client('s3')
        v2_framework_dict = json.loads(os.environ['v2_framework'])
        target_bucket = v2_framework_dict['target_bucket']
        v2_curated_bucket =  v2_framework_dict['curated_bucket']
        stage_bucket = v2_framework_dict['stage_bucket']
        key_out_path = v2_framework_dict['key_out_path']
        bucket = v2_framework_dict['stage_bucket']
        file_path = v2_framework_dict['file_path']
        cb_app_folder = v2_framework_dict['unzip_path3']
        # bucket = "cci-edo-data-source"
        print("data mapping key",bucket, key, jobid)
        fname = key.replace(cb_app_folder,'')
        key_fl_chk = key_fl_chk.replace('.tsv', '.parquet')
        key_out = key_out_path+'DT_FILE_DT='+match+'/'+key_fl_chk
        existing_buffer = io.BytesIO()
        s3_client.download_fileobj(bucket, key, existing_buffer)
        existing_buffer.seek(0)
        existing_data = pd.read_csv(existing_buffer, sep = '\t',encoding='ISO-8859-1')
        df = existing_data
        # update_cif_job_status_record(rds_cur, cif_id, len(df), cron_details, error_message, error_flag="N")
        if not cif_id:
            update_cif_job_status_record(rds_cur, cif_id, len(df), '', key, 'Y')
            raise exception(str("cif not found"))
        update_cif_job_status_record(rds_cur, cif_id, len(df), '', key, 'CUSTOM')
        print("data mapping df head",df.head(2))
        update_file_log(rds_cur, "IN PROGRESS", "DICT MAPPING STARTED", "DICT MAPPING IN DATAFRAME", fname, jobid)
        
        for file_chk in data_file:
            if 'dict_browser' in file_chk:
                print("yes its there", len(data_file))
                dict_browser = file_chk['dict_browser']
                df['browser']= df['browser'].map(dict_browser)
            # elif 'dict_browser_type' in file_chk:
            #     print("yes its there", len(data_file))
            #     dict_browser_type = file_chk['dict_browser_type']
            #     df['browser_type']= df['browser_type'].map(dict_browser_type)
            elif 'dict_color_depth' in file_chk:
                print("yes its there color_depth")
                # dict_browser_type = file_chk['dict_browser_type']
                df['c_color']= df['c_color'].map(dict_color_depth)
            elif 'dict_resolution' in file_chk:
                print("yes its there resolution")
                dict_resolution = file_chk['dict_resolution']
                df['resolution']= df['resolution'].map(dict_resolution)
            elif 'dict_referrer_type' in file_chk:
                print("yes its there dict_referrer_type")
                dict_referrer_type = file_chk['dict_referrer_type']
                df['first_hit_ref_type']= df['first_hit_ref_type'].map(dict_referrer_type)
            elif 'dict_plugins' in file_chk:
                print("yes its there dict_plugins")
                dict_plugins = file_chk['dict_plugins']
                df['plugins']= df['plugins'].map(dict_plugins)
            elif 'dict_operating_systems' in file_chk:
                print("yes its there dict_operating_systems")
                dict_operating_systems = file_chk['dict_operating_systems']
                df['os']= df['os'].map(dict_operating_systems)
            elif 'dict_language' in file_chk:
                print("yes its there dict_language")
                dict_language = file_chk['dict_language']
                df['language']= df['language'].map(dict_languages)
            elif 'dict_javascript' in file_chk:
                print("yes its there dict_javascript")
                dict_javascript = file_chk['dict_javascript']
                df['javascript']= df['javascript'].map(dict_javascript)
            elif 'dict_event_list' in file_chk:
                print("yes its there dict_event_list")
                dict_event_list = file_chk['dict_event_list']
                df['event_list']= df['event_list'].map(dict_event_list)
            elif 'dict_connection_type' in file_chk:
                print("yes its there connection_type")
                dict_connection_type = file_chk['dict_connection_type']
                df['connection_type']= df['connection_type'].map(dict_connection_type)
            elif 'dict_country' in file_chk:
                print("yes its there country")
                dict_country = file_chk['dict_country']
                df['country']= df['country'].map(dict_country)
            elif 'dict_search_engine' in file_chk:
                print("yes its there dict_search_engine")
                dict_search_engine = file_chk['dict_search_engine']
                df['search_engine']= df['search_engine'].map(dict_search_engines)
        df['file_dt'] = match
        print("inside data mapping, convert to parquet")
        df['browser']= df['browser'].astype(str)
        df['c_color']= df['c_color'].astype(str)
        df['resolution']= df['resolution'].astype(str)
        df['first_hit_ref_type']= df['first_hit_ref_type'].astype(str)
        df['plugins']= df['plugins'].astype(str)
        df['os']= df['os'].astype(str)
        df['language']= df['language'].astype(str)
        df['javascript']= df['javascript'].astype(str)
        df['event_list']= df['event_list'].astype(str)
        df['connection_type']= df['connection_type'].astype(str)
        df['country']= df['country'].astype(str)
        df['search_engine']= df['search_engine'].astype(str)
        df['geo_zip'] = pd.to_numeric(df['geo_zip'], errors='coerce').astype('Int64')
        df['mobile_id'] = pd.to_numeric(df['mobile_id'], errors='coerce').astype('Int64')
        df['browser_height'] = pd.to_numeric(df['browser_height'], errors='coerce').astype('Int64')
        out_buffer = io.BytesIO()
        
        df.to_parquet(out_buffer, index=False)
        
        print("out", key_out)
        out_buffer.seek(0)
        print("out s3", v2_curated_bucket)
        s3_client.put_object(Bucket=v2_curated_bucket, Key=key_out, Body=out_buffer.getvalue())
        print("out s3 rds_cur")
        update_file_log(rds_cur, "IN PROGRESS", "DICT MAPPING DONE", "DICT MAPPING IN DATAFRAME", fname, jobid)
        return match, len(df)
        # print("existing_data",existing_data.head(2))
    except Exception as e:
        print("Error data_mapping",str(e))
        # rds_conn.close()
        update_file_log(rds_cur, "FAILED", "DICT MAPPING FAILED", "DICT MAPPING IN DATAFRAME", fname, jobid)
        logger.error("Function Name: {} Error: {}".format("data_mapping", str(e)))
        
        
def dict_dataframe(files, archive, jobid):
    try:
        print("dict_dataframe ", files, archive, jobid)
        global browser, browser_type, color_depth, resolution, referrer_type, plugins, operating_systems, languages, javascript_version, event, connection_type, country, search_engines
        
        global dict_browser,dict_browser_type,dict_color_depth, dict_resolution, dict_referrer_type, dict_plugins, dict_operating_systems, dict_languages
        global dict_javascript_version, dict_event, dict_connection_type, dict_country, dict_search_engines
        # update_file_log(rds_cur, "IN PROGRESS", "DICT DATAFRAME STARTED", "DICT CREATION IN DATAFRAME", file_defination_nm)
        update_file_log(rds_cur, "ONGOING", "DICT STARTED", "DICT IN DATAFRAME", files, jobid)
        v2_framework_dict = json.loads(os.environ['v2_framework'])
        v2_curated_bucket =  v2_framework_dict['curated_bucket']
        key_out1_path = v2_framework_dict['key_out1_path']
        df_len = 0
        df = pd.DataFrame()
        if 'browser.tsv' in files:
            print("files",files)
            df_browser = pd.read_csv(archive.extractfile(files),header = None, index_col=False, sep ='\t',encoding='ISO-8859-1')
            df_browser.columns = ['browser_id','browser_value']
            print("df_browser",df_browser.head(2))
            df_len = len(df_browser)
            df = df_browser
            print("browser len", df_len)
            dict_browser = dict_files(df_browser,files)
            # print("df_dict_browser", dict_browser)
            print("df_dict_browser files", files)
            list_lookup.append({'dict_browser': dict_browser})
        elif 'browser_type.tsv' in files:
            print("files",files)
            df_browser_type = pd.read_csv(archive.extractfile(files),header=None, index_col=False, sep ='\t',encoding='ISO-8859-1')
            df_len = len(df_browser_type)
            print("browser type len", df_len)
            print("df_browser_type",df_browser_type.head(2))
            df_browser_type.columns = ['browser_type_id','browser_type_value']
            df = df_browser_type
            dict_browser_type = dict_files(df_browser_type,files)
            list_lookup.append({'dict_browser_type': dict_browser_type})
            # print("dict called", dict_files(df_browser_type,files))
        elif 'color_depth.tsv' in files:
            print("files",files)
            df_color_depth = pd.read_csv(archive.extractfile(files),header=None, index_col=False, sep ='\t',encoding='ISO-8859-1')
            df_len = len(df_color_depth)
            df_color_depth.columns = ['color_depth_id','color_depth_value']
            df = df_color_depth
            print("df_color_depth",df_color_depth.head(2))
            dict_color_depth = dict_files(df_color_depth,files)
            list_lookup.append({'dict_color_depth':dict_color_depth})
            # print("dict called", dict_files(df_color_depth,files))
        elif 'resolution.tsv' in files:
            print("files",files)
            df_resolution = pd.read_csv(archive.extractfile(files),header=None, index_col=False, sep ='\t',encoding='ISO-8859-1')
            df_len = len(df_resolution)
            df_resolution.columns = ['resolution_id','resolution_value']
            print("df_resolution",df_resolution.head(2))
            df = df_resolution
            dict_resolution = dict_files(df_resolution,files)
            df = df_resolution
            list_lookup.append({'dict_resolution':dict_resolution})
            # print("dict called", dict_files(df_resolution,files))
        elif 'referrer_type.tsv' in files:
            print("files",files)
            df_referrer_type = pd.read_csv(archive.extractfile(files),header=None, index_col=False, sep ='\t',encoding='ISO-8859-1')
            df_referrer_type.columns = ['referrer_type_id','referrer_type_value', 'referrer_type_value2']
            df_len = len(df_referrer_type)
            df = df_referrer_type
            print("df_referrer_type",df_referrer_type.head(2))
            dict_referrer_type = dict_files(df_referrer_type,files)
            list_lookup.append({'dict_referrer_type':dict_referrer_type})
            # print("dict called", dict_files(df_referrer_type,files))
        elif 'plugins.tsv' in files:
            print("files",files)
            df_plugins = pd.read_csv(archive.extractfile(files),header=None, index_col=False, sep ='\t', encoding='ISO-8859-1')
            df_plugins.columns = ['plugins_id','plugins_value']
            df = df_plugins
            df_len = len(df_plugins)
            print("df_plugins",df_plugins.head(2))
            dict_plugins = dict_files(df_plugins,files)
            list_lookup.append({'dict_plugins':dict_plugins})
            # print("dict called", dict_files(df_plugins,files))
        elif 'operating_systems.tsv' in files:
            print("files",files)
            df_operating_systems = pd.read_csv(archive.extractfile(files),header=None, index_col=False, sep ='\t',encoding='ISO-8859-1')
            df_operating_systems.columns = ['operating_systems_id','operating_systems_value']
            df = df_operating_systems
            print("df_operating_systems",df_operating_systems.head(2))
            df_len = len(df_operating_systems)
            dict_operating_systems = dict_files(df_operating_systems,files)
            list_lookup.append({"dict_operating_systems":dict_operating_systems})
            # print("dict called", dict_files(df_operating_systems,files))
        elif 'languages.tsv' in files:
            print("files",files)
            df_languages = pd.read_csv(archive.extractfile(files),header=None, index_col=False, sep ='\t',encoding='ISO-8859-1')
            df_languages.columns = ['languages_id','languages_value']
            df = df_languages
            df_len = len(df_languages)
            print("df_languages",df_languages.head(2))
            dict_languages = dict_files(df_languages,files)
            list_lookup.append({"dict_languages":dict_languages})
            # print("dict called", dict_files(df_languages,files))
        elif 'javascript_version.tsv' in files:
            print("files",files)
            df_javascript_version = pd.read_csv(archive.extractfile(files),header=None, index_col=False, sep ='\t',encoding='ISO-8859-1')
            df_javascript_version.columns = ['javascript_version_id','javascript_version_value']
            df = df_javascript_version
            df_len = len(df_javascript_version)
            print("df_javascript_version",df_javascript_version.head(2))
            dict_javascript_version = dict_files(df_javascript_version,files)
            list_lookup.append({"dict_javascript_version":dict_javascript_version})
            # print("dict called", dict_files(df_javascript_version,files))
        elif 'event.tsv' in files:
            print("files",files)
            
            df_event = pd.read_csv(archive.extractfile(files),header=None, index_col=False, sep ='\t',encoding='ISO-8859-1')
            
            df_event.columns = ['event_id','event_value']
            df = df_event
            df_len = len(df_event)
            print("df_event",df_event.head(2))
            dict_event = dict_files(df_event,files)
            list_lookup.append({"dict_event":dict_event})
            # print("dict called", dict_files(df_event,files))
        elif 'connection_type.tsv' in files:
            print("files",files)
            df_connection_type = pd.read_csv(archive.extractfile(files),header=None, index_col=False, sep ='\t',encoding='ISO-8859-1')
            df_connection_type.columns = ['connection_type_id','connection_type_value']
            df = df_connection_type
            df_len = len(df_connection_type)
            print("df_connection_type",df_connection_type.head(2))
            dict_connection_type = dict_files(df_connection_type,files)
            list_lookup.append({"dict_connection_type":dict_connection_type})
            # print("dict called", dict_files(df_connection_type,files))
        elif 'country.tsv' in files:
            print("files",files)
            df_country = pd.read_csv(archive.extractfile(files),header=None, index_col=False, sep ='\t',encoding='ISO-8859-1')
            df_country.columns = ['country_id','country_value']
            df = df_country
            df_len = len(df_country)
            print("df_country",df_country.head(2))
            dict_country = dict_files(df_country,files)
            list_lookup.append({"dict_country":dict_country})
            # print("dict called", dict_country)
        elif 'search_engines.tsv' in files:
            print("files",files)
            df_search_engines = pd.read_csv(archive.extractfile(files),header=None, index_col=False, sep ='\t',encoding='ISO-8859-1')
            df_search_engines.columns = ['search_engines_id','search_engines_value']
            df = df_search_engines
            df_len = len(df_search_engines)
            print("df_search_engines",df_search_engines.head(2))
            dict_search_engines = dict_files(df_search_engines,files)
            list_lookup.append({"dict_search_engines":dict_search_engines})
            # print("dict called", dict_files(df_search_engines,files))
        key_fl_chk = files.replace('.tsv', '.parquet')
        print("data dict frame",df.head(2), len(df))
        # if 'event' in files:
        #     files = files.replace("event", 'events')
        files_repl = files.replace('.tsv','')
        key_out1 = key_out1_path+files_repl+'/'+key_fl_chk
        s3_client = boto3.client('s3')
        out_buffer = io.BytesIO()
        df.to_parquet(out_buffer, index=False)
        
        print("out", key_out1, files, len(df))
        out_buffer.seek(0)
        print("out s3", v2_curated_bucket)
        s3_client.put_object(Bucket=v2_curated_bucket, Key=key_out1, Body=out_buffer.getvalue())
        # if 'event' in files:
        #     files = files.replace("events", 'event')
        update_file_log(rds_cur, "COMPLETED", "DICT STARTED", "DICT IN DATAFRAME", files, jobid)
        print("list_lookup", files)
        return df_len , list_lookup
    except Exception as e:
        print("Error : DICT CREATION IN DATAFRAME ", str(e))
        logger.error("Function Name: {} Error: {}".format("dict_dataframe", str(e)))
        # update_file_log(rds_cur, "FAILED", "DICT DATAFRAME FAILED", "DICT CREATION IN DATAFRAME", file_defination_nm)
        print("Error dict dataframe",str(e))

def insert_file_log(cursor, file_defination_nm1,job_run_ids):
    """
    This function is used to make an entry in FILE_LOG table.
    :param cursor: Python Cursor Object to execute SQL queries in RDS.
    :return: None.
    """

    try:
        logger.info(
            "Inside insert_file_log function. Process started to insert an entry in FILE_LOG table."
        )
        print("file_defination_nm1--",file_defination_nm1)
        # Inserting an entry in FILE_LOG table
        cursor.execute(
            f"INSERT INTO {rds_file_log}(file_definition_id, file_definition_nm, file_description, "
            f"file_process_status, file_dt, create_dt, last_update_dt, job_id, stage) "
            f"VALUES('CBAPP', '{file_defination_nm1}', '{file_defination_nm1}', "
            f"'STARTED', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), "
            f"CURRENT_TIMESTAMP(), '{job_run_ids}', 'STARTED');"
        )
        
        
        logger.info(
            "Inside insert_file_log function. Process completed to insert an entry in FILE_LOG table."
        )
        return job_run_id

    except Exception as e:
        logger.error(
            f"Error encountered in insert_file_log function.\nError: {str(e)}"
        )
        sys.exit()


def update_file_log(cursor, statuser, stage, error_msg, file_defination_nm, job_run_id1):
    """
    This function is used to make an entry in FILE_LOG table.
    :param cursor: Python Cursor Object to execute SQL queries in RDS.
    :param status: Python String representing FILE_PROCESS_STATUS.
    :param stage: Python String representing STAGE.
    :param error_msg: Python String representing the error message.
    :return: None.
    """

    try:
        logger.info(
            "Inside update_file_log function. Process started to update entry in FILE_LOG table."
        )

        # Formatting the error message
        error_msg = error_msg.replace("'", "").replace('"', "")

        # Inserting an entry in FILE_LOG table
        cursor.execute(
            f"UPDATE {rds_file_log} SET file_process_status='{statuser}', "
            f"last_update_dt=CURRENT_TIMESTAMP(), error_msg='{error_msg}', "
            f"stage='{stage}' WHERE file_definition_id='CBAPP' "
            f"AND file_definition_nm='{file_defination_nm}' "
            f"AND job_id='{job_run_id1}';"
        )

        logger.info(
            "Inside update_file_log function. Process completed to update entry in FILE_LOG table."
        )

    except Exception as e:
        logger.error(
            f"Error encountered in update_file_log function.\nError: {str(e)}"
        )


def check_file_processed(cursor, file_nm, status):
    """
    This function is used to check an entry in FILE LOG table for processed status.
    :param cursor: Python Cursor Object to execute SQL queries in RDS.
    :return: None.
    """

    try:
        logger.info(
            "Inside check_file_process for processed status. Process started to check an entry in FILE_LOG table."
        )

        
        # print("file name inside func file process", file_nm, rds_file_log)
        resp = cursor.execute(
            f"SELECT COUNT(*) from {rds_file_log} WHERE FILE_DESCRIPTION = '{file_nm}' AND FILE_DEFINITION_ID = 'CBAPP' AND FILE_DEFINITION_NM = '{file_nm}' AND FILE_PROCESS_STATUS = '{status}';"
        )
        
        print("resp-->",resp)
        response = cursor.fetchall()[0][0]
        print("resp_fetchall-->", response)
        # print("resp_fetchall-->",cursor.fetchmany())
        
        logger.info(
            "Inside check_file_process for processed status. Process started to check an entry in FILE_LOG table."
        )
        return response

    except Exception as e:
        logger.error(
            f"Error encountered in check_file_process function.\nError: {str(e)}"
        )
        sys.exit()


def insert_cif_job_status_record(cursor, file_nm, table_names):
    """
    Function to insert cig_job_status record in database for v2 process
    :return:
    """
    
    global_database_name = os.environ['global_database_name']
    global_job_name = os.environ['global_job_name']
    db_details = json.loads(os.environ['DB_DETAILS'])
    cfg_database_name = db_details['cfg_database_name']
    schema_name = db_details['schema_name']
    table_name = table_names
    try:
        # insert into cif table
        print("cursor, file_nm, table_names--", cursor, file_nm, table_names)
        table_json = str(json.dumps(
            {"jobName": global_job_name, "dbName": cfg_database_name.upper(), "dbSchema": schema_name.upper(),
             "dbTable": table_name.upper(), "file_nm":file_nm}))
        # print("table_json", table_json)
        onprem_desc_json_new = str(json.dumps({"status": "IN PROGRESS", "reason_cd": "NONE", "run_cnt": "1"}))

        cif_columns = ['TABLE_JSON', 'MANUAL_FLG', 'ONPREM_DESC_JSON', 'ONPREM_STRT_TM', 'CREATE_DT', 'LAST_UPD_DT']
        cif_args = ["\'" + table_json + "\'", "\'N\'", "\'" + onprem_desc_json_new + "\'",
                    "\'" + str(datetime.now())[:-7] + "\'", "\'" + str(datetime.now())[:-7] + "\'",
                    "\'" + str(datetime.now())[:-7] + "\'"]
        cif_insert_query = "INSERT INTO {}.{} ({}) VALUES ({});".format(
            global_database_name, 'cif_job_status', ','.join(cif_columns), ','.join(cif_args))
        logger.info(cif_insert_query)
        # Formatting the error message
        # error_msg = error_msg.replace("'", "").replace('"', "")

        # Inserting an entry in FILE_LOG table
        cursor.execute(
            cif_insert_query
        )
        # cursor = execute_sql_query(global_db_connection, cif_insert_query, True)
        
        cif_id = cursor.lastrowid
        print("cif_id", cif_id)
        # output = cursor.fetchall()
        # print("output insert cif", output)
        return cif_id
    except Exception as exception:
        print("error insert_cif_job_status_record", str(exception))
        logger.error("Function Name: {} Error: {}".format("insert_cif_job_status_record" ,str(exception)))
        raise Exception(str(exception))


def update_cif_job_status_record(rds_cur, cif_id, count_dict, cron_details, error_message, error_flag):
    """
    Function to update cif_job_status record in database for v2 process
    :param count_dict:
    :return:
    """
    try:
        global_database_name = os.environ['global_database_name']
        # calculate total count of all partitions
        if count_dict:
            total_count = count_dict
        # update cif table
        print("error_flag", error_flag, error_message, count_dict, cif_id, cron_details)
        if error_flag == "N":
            cloud_stats = 'COMPLETED'
            onprem_desc_json_upd = str(json.dumps({"status": "COMPLETED", "reason_cd": "NONE", "run_cnt": "1"}))
            
        elif error_flag == "Y":
            onprem_desc_json_upd = {"status": "FAILED", "reason_cd": "NONE", "run_cnt": "1"}
            cloud_stats = 'FAILED'
            error_message = error_message.replace("\n", "")
            error_message = error_message.replace("'",'')
            error_message = error_message.strip()
            print("error_message",error_message)
            onprem_desc_json_upd["reason_cd"] = error_message
            onprem_desc_json_upd = str(json.dumps(onprem_desc_json_upd))
        # elif error_flag == "CUSTOM":
        #     onprem_desc_json = {"status": "IN PROGRESS", "reason_cd": "NONE", "run_cnt": "1"}
        #     cloud_stats = 'IN PROGRESS'
        #     error_message = error_message.replace("\n", "")
        #     error_message = error_message.replace("'",'')
        #     error_message = error_message.strip()
        #     print("error_message",error_message)
        #     onprem_desc_json["reason_cd"] = error_message
        #     onprem_desc_json = str(json.dumps(onprem_desc_json))

        # calculate next scheduled run time
        if cron_details:
            cron_expression = cron_details['frequency']
            cron_type = cron_details['schedule_TYPE'].lower()
            aws_cron = AWSCron(cron_expression)
            now = datetime.now()
            if cron_type == 'cron':
                utc_now = datetime(now.year, now.month, now.day, now.hour, now.minute,
                                            tzinfo=datetime.timezone.utc)
                next_sch_time = str(aws_cron.occurrence(utc_now).next()).split('+')[0]
            elif cron_type == 'rate':
                cron_rate_value = cron_expression.split(' ')[0]
                cron_rate_freq = cron_expression.split(' ')[1]
                if cron_rate_freq in 'days':
                    next_sch_time = str(now + timedelta(days=cron_rate_value))[:-7]
                if cron_rate_freq in 'hours':
                    next_sch_time = str(now + timedelta(hours=cron_rate_value))[:-7]
                if cron_rate_freq in 'minutes':
                    next_sch_time = str(now + timedelta(minutes=cron_rate_value))[:-7]
        else:
            next_sch_time = str(datetime.now())[:-7]
        
        print("count_dict", count_dict)
        if count_dict:
            print("status count", cloud_stats, onprem_desc_json_upd)
            cif_update_query = rds_cur.execute(
            f"UPDATE {global_database_name}.cif_job_status SET CLOUD_STS='{cloud_stats}', CLOUD_STRT_TM= '{str(datetime.now())[:-7]}', "
            f"ONPREM_CNT={total_count}, ONPREM_DESC_JSON='{onprem_desc_json_upd}',  CLOUD_END_TM= '{str(datetime.now())[:-7]}', "
            f"ONPREM_END_TM='{str(datetime.now())[:-7]}', ONPREM_NXT_SCH_TM='{next_sch_time}', "
            f"LAST_UPD_DT='{str(datetime.now())[:-7]}' WHERE ID={cif_id} ")
            logger.info(cif_update_query)
            # cif_update_query = "UPDATE {}.{} SET CLOUD_STS = \"{}\", ONPREM_CNT = \"{}\", ONPREM_DESC_JSON = \'{}\', ONPREM_END_TM = \"{}\", ONPREM_NXT_SCH_TM = \"{}\", LAST_UPD_DT = \"{}\" WHERE ID = {}".format(
            #     global_database_name,
            #     'cif_job_status', cloud_stats, total_count, onprem_desc_json, str(datetime.now())[:-7], next_sch_time, cloud_stats,
            #     str(datetime.now())[:-7], cif_id)
        else:
            print("status not count", cloud_stats, onprem_desc_json_upd)
            cif_update_query = rds_cur.execute(
            f"UPDATE {global_database_name}.cif_job_status SET CLOUD_STS='{cloud_stats}', CLOUD_STRT_TM= '{str(datetime.now())[:-7]}', "
            f"ONPREM_DESC_JSON='{onprem_desc_json_upd}',  CLOUD_END_TM= '{str(datetime.now())[:-7]}', "
            f"ONPREM_END_TM='{str(datetime.now())[:-7]}', ONPREM_NXT_SCH_TM='{next_sch_time}', "
            f"LAST_UPD_DT='{str(datetime.now())[:-7]}' WHERE ID={cif_id} ")
            logger.info(cif_update_query)
            # cif_update_query = "UPDATE {}.{} SET CLOUD_STS = \"{}\", ONPREM_DESC_JSON = \'{}\', ONPREM_END_TM = \"{}\", ONPREM_NXT_SCH_TM = \"{}\",  LAST_UPD_DT = \"{}\" WHERE ID = {}".format(
            #     global_database_name,
            #     'cif_job_status', cloud_stats, onprem_desc_json, str(datetime.now())[:-7], next_sch_time, 
            #     str(datetime.now())[:-7], cif_id)
        # logger.info(cif_update_query)
        print("cif_update_query---- query updated", cif_id)
        # rds_cur.execute(cif_update_query)
        # cursor = execute_sql_query(global_db_connection, cif_update_query, True)
    except Exception as exception:
        print("error update_cif_job_status_record", str(exception))
        logger.error("Function Name: {} Error: {}".format("update_cif_job_status_record", str(exception)))
        raise Exception(str(exception))
        

def get_cron_details(db_connection, job_name, database_name, metadata_table_name):
    """
    Function to get the cron details from the metadata table
    :param db_connection:
    :param job_name:
    :param database_name:
    :param metadata_table_name:
    :return:
    """
    try:
        get_cron_sql = "SELECT CRON_JSON FROM " + database_name + "." + metadata_table_name + \
                       " where JOB_NM = '" + job_name + "';"
        # cron_json_cursor = execute_sql_query(db_connection, get_cron_sql)
        cursor.execute(
            get_cron_sql
        )
        for row in cron_json_cursor:
            cron_json = row[0]
        cron_json = json.loads(str(cron_json))
        logger(cron_json)
    except Exception as exception:
        logger("Function Name: {} Error: {}".format(get_cron_details.__name__, str(exception)))
        raise Exception(str(exception))
    return cron_json

# ************************************* V2 MODULE****************************************************
def initiate_v2_process(df_count, cif_id, v2_load_type, partition_key, table_name):
    """
    Function to kick start v2 process
    :param df_count:
    :return:
    """
    try:
        logger.info('Initiating V2 process')
        print("V2_handshake_flag df_count", df_count, type(df_count), table_name)
        print("V2_handshake_flag cif_id", cif_id, type(cif_id))
        # Get the required values from configuration
        # print("os environ v2", os.environ['v2_framework'], type(os.environ['v2_framework']))
        print(json.loads(os.environ['v2_framework']))
        v2_framework_dict = json.loads(os.environ['v2_framework'])
        print("os environ ['handshake_flag']", v2_framework_dict)
        print("os environ ['handshake_flag'ttt]", v2_framework_dict['handshake_flag'])
        v2_handshake_flag = v2_framework_dict['handshake_flag'].strip().lower()
        print("V2_handshake_flag", v2_handshake_flag)
        # v2_handshake_flag = str(
        #     get_json_value(global_configuration_details, ['v2_framework', 'handshake_flag'])).lower()
        dfcount = {}
        # Check job has v2 process
        if v2_handshake_flag == "y":
            logger.info('V2 Handshake is Y')
            print('df_count V2',df_count)
            create_v2_metadata(v2_load_type, partition_key, table_name)
            print('df_count V2 after meta',df_count)
            create_v2_done_file(df_count, cif_id,v2_load_type, partition_key, table_name)
        print("V2_done")
    except Exception as exception:
        # rds_conn.close()
        print("Exception in initiating v2 process, Exception - {}", str(exception))
        logger.error("Exception in initiating v2 process, Exception - {}".format(exception))
        raise Exception("Exception in initiating v2 process, Exception - {}".format(exception))


def create_v2_done_file(count_dict, cif_id, v2_load_type, partition_key, table_name):
    """
    Function to create done file for v2 process
    :param count_dict:
    :param cif_id:
    :return:
    """
    try:
        logger.info('Inside V2 done file creation function')
        print("inside v2_load_ count_dict", count_dict, cif_id)
        s3_client = boto3.client('s3')
        v2_framework_dict = json.loads(os.environ['v2_framework'])
        # v2_load_type = v2_framework_dict['load_type'].lower()
        print("v2_load_type---V2", v2_load_type)
        db_details = json.loads(os.environ['DB_DETAILS'])
        database_name = db_details['cfg_database_name']
        schema_name = db_details['schema_name']
        # table_name = db_details['table_name']
        # partition_key = v2_framework_dict['partition_key']
        v2_done_bucket = v2_framework_dict['done_bucket']
        v2_done_file_path = v2_framework_dict['done_file_path']
        print("count_dict",count_dict)
        # print("count_dict", count_dict)
        if len(count_dict)>0:
            if v2_load_type == 'partitioned':
                # count comes in as a dictionary with partitioned tables
                partition_list = []
                # key is date and value is count
                for key, value in count_dict.items():
                    if key==None:
                        pass
                    else:
                        print("key, value v2 done",key,value)
                        partition_row = ' | '.join(
                            [database_name.upper(), schema_name.upper(), table_name.upper(), v2_load_type.upper(),
                            partition_key, str(key), str(value)])
                        partition_list.append(partition_row)
                        logger.info('Partition row: {}'.format(partition_row))
                done_file_body = '\n'.join(partition_list)
                done_file_name = '.'.join(
                    [database_name, schema_name, table_name, datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3],
                    str(cif_id), 'done'])
            elif v2_load_type == 'full':  # count comes in as an int with full tables
                for key, value in count_dict.items():
                    if key==None:
                        pass
                    else:
                        print("key, value v2 done full",key,value)
                        # total_count = count_dict['FULL']
                        done_file_body = ' | '.join(
                            [database_name.upper(), schema_name.upper(), table_name.upper(), v2_load_type.upper(), '', str(key),
                            str(value)])
                        done_file_name = '.'.join(
                            [database_name, schema_name, table_name, datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3],
                            str(cif_id), 'done'])
            else:
                logger.info('V2 load type missing or incorrectly specified. Review metadata information.')
                raise Exception('V2 load type missing or incorrectly specified. Review metadata information.')

            logger.info(done_file_body)
            
            s3_client.put_object(Body=done_file_body, Bucket=v2_done_bucket,
                                Key=v2_done_file_path + '/' + database_name + '/' + schema_name + '/' + table_name + '/' + done_file_name)
            print("done file path", v2_done_bucket, v2_done_file_path + '/' + database_name + '/' + schema_name + '/' + table_name + '/' + done_file_name)
            print("table name", table_name)
        else:
            #NOTE - NO DONE FILE WILL BE CREATED
            print("NO DONE FILE WILL BE CREATED"+str(count_dict))
            logger.info('No data to be processed')
            pass

        
    except Exception as exception:
        print("Exception in create_v2_done_file", str(exception))
        # rds_conn.close()
        logger.error("Function Name: {} Error: {}".format("create_v2_done_file", str(exception)))
        raise Exception(str(exception))
        

def create_v2_metadata(v2_load_type, partition_key, table_name):
    """
    Function to add entry in v2 metadata table for v2 process
    :return:
    """
    logger.info('Inside Create V2 metadata function')
    # source_type = str(get_json_value(global_configuration_details, ['source', 'type'])).lower().strip()
    source_type = 's3'
    v2_framework_dict = json.loads(os.environ['v2_framework'])
    global_database_name = os.environ['global_database_name']
    # cfg_database_name = os.environ['cfg_database_name']
    # schema_name = os.environ['schema_name']
    # table_name = os.environ['table_name']
    
    db_details = json.loads(os.environ['DB_DETAILS'])
    cfg_database_name = db_details['cfg_database_name']
    schema_name = db_details['schema_name']
    # table_name = db_details['table_name']
    app_nm = db_details['app_nm']
    domain_nm = db_details['domain_nm']
    # v2_load_type = v2_framework_dict['load_type'].lower()
    # partition_key = get_json_value(global_configuration_details, ['partition_key'])
    # partition_key = v2_framework_dict['partition_key']
    partition_key_rdbms = v2_framework_dict['partition_key_rdbms']
    target_bucket = v2_framework_dict['target_bucket']
    v2_curated_bucket =  v2_framework_dict['curated_bucket']
    v2_execution_group =  v2_framework_dict['execution_group']
    v2_lakeformation_flag =  v2_framework_dict['lakeformation_flag']
    v2_curated_bucket_path =  v2_framework_dict['v2_curated_bucket_path']
    v2_encrypt_src_flag =  v2_framework_dict['encrypt_src_flag']
    v2_timestamp_partition =  v2_framework_dict['timestamp_partition'].upper()
    v2_config_json = json.loads(os.environ['v2_config_json'])
    target_bucket_prefix =v2_framework_dict['target_bucket_prefix']
    # target_bucket_prefix = get_json_value(global_configuration_details, ['target_bucket_prefix'])
    # aws_eds_db = 'v2dataframework'
    aws_eds_db =  v2_framework_dict['aws_eds_db']
    aws_acoe_db =  v2_framework_dict['aws_acoe_db']
    aws_cona_db =  v2_framework_dict['aws_cona_db']
    downstream= {
      "handshake": "Y",
      "downstream_bucket": "cci-edo-data-ingeststatus",
      "downstream_s3_path": "handshake/downstream/de-po/"}
    downstream_handshake = downstream['handshake']
    downstream_s3_path = downstream['downstream_s3_path']
    downstream_bucket = downstream['downstream_s3_path']
    # key_out = 'raw/aws/webanalytics/cbapp/'+'DT_FILE_DT='+match+'/'+key_fl_chk
    v2_curated_bucket_path = cfg_database_name + '/' + schema_name + '/' + table_name if v2_curated_bucket_path=="" else v2_curated_bucket_path
    lakeformation_flag = "N" if v2_lakeformation_flag=="" else v2_lakeformation_flag
    try:
        # check if metadata entry already exists
        metadata_check_query = "SELECT * FROM {}.{} WHERE RDBMS_DB_NAME = \'{}\' and RDBMS_SCHEMA_NAME = \'{}\' and RDBMS_TBL_Name = \'{}\' ;" \
            .format(global_database_name, 'RDBMS_S3_DATA_INGESTION_CFG', cfg_database_name, schema_name, table_name)
        print(metadata_check_query)
        # output = execute_sql_query(global_db_connection, metadata_check_query)
        print("rds_cur", rds_cur)
        rds_cur.execute(metadata_check_query)
        # cursor = execute_sql_query(global_db_connection, cif_insert_query, True)
        output = rds_cur.fetchall()
        # print('output metadata',output, type(output), len(output))
        if len(output) > 0:
            if partition_key_rdbms == "":
                partition_key_rdbms = 'N'
            else:
                partition_key_rdbms = 'Y'
            if partition_key == '':
                partition_flag = 'N'
            else:
                partition_flag = 'Y'
            if v2_timestamp_partition != 'Y':
                v2_timestamp_partition = 'N'
            raw_table = table_name + '_raw'
            s3_raw_full_bucket_path = 's3://' + target_bucket + '/' + target_bucket_prefix + '/' + cfg_database_name + '/' + schema_name + '/' + table_name
            s3_curate_full_bucket_path = 's3://' + v2_curated_bucket + '/' + v2_curated_bucket_path
            
            logger.info('RDBMS Config already exists for table')
            existing_json = v2_config_json
            # existing_json = json.loads(v2_config_json)
            # print('existing_json',existing_json)
            existing_json['downstream'] = {
                "s3_path": downstream_s3_path,
                "handshake": downstream_handshake,
                "done_bucket": downstream_bucket
            }
            print('lakeformation_flag--->123',lakeformation_flag)
            if lakeformation_flag=="Y":
                updated_json = json.dumps(existing_json)
                # print('updated_json',updated_json)
                rdbms_update_query = f"""UPDATE {global_database_name}.RDBMS_S3_DATA_INGESTION_CFG SET LOAD_TABLE_CFG='N',RDBMS_DB_NAME='{cfg_database_name}', RDBMS_SCHEMA_NAME='{schema_name}', RDBMS_TBL_Name='{table_name}',
                                    DataLoadTool='LF', RDBMS_TBL_PARTITIONED='{partition_key_rdbms}',
                                    AWS_TBL_PARTITIONED='{partition_flag}', RDBMS_PARTITIONED_Col='{partition_key}', RAW_TABLE='{raw_table}', S3_RAW_FULL_BUCKET_PATH='{s3_raw_full_bucket_path}',
                                    STAGE_TABLE='', S3_STAGE_FULL_BUCKET_PATH='',
                                    CURATED_TABLE='{table_name}', S3_CURATE_FULL_BUCKET_PATH='{s3_curate_full_bucket_path}', RDBMS_REFRESH_STATUS='2',
                                    RDBMS_EXEC_GROUP='{v2_execution_group}', AWS_EDS_DB='{aws_eds_db}', AWS_ACOE_DB='{aws_acoe_db}', AWS_CONA_DB='{aws_cona_db}',
                                    ONPREM_PREFIX='DT_', TIMESTAMP_PARTITION_FLAG='{v2_timestamp_partition}', encrypt_src_flag='{v2_encrypt_src_flag}', CONFIG_JSON='{updated_json}',
                                    LAKEFORMATION_ENABLED_FLAG_ACOE_N='Y', LAKEFORMATION_ENABLED_FLAG_CA_N='Y',
                                    LAKEFORMATION_ENABLED_FLAG_ACOE_SB='Y', LAKEFORMATION_ENABLED_FLAG_CA='Y', LAKEFORMATION_ENABLED_FLAG_ACOE='Y',DOMAIN_NAME='{domain_nm}',APPLICATION_NAME='{app_nm}'
                        WHERE (RDBMS_SCHEMA_NAME = '{schema_name}') and (RDBMS_TBL_Name = '{table_name}');"""
                # print("rd34",rdbms_update_query)
                rds_cur.execute(rdbms_update_query)
                # cursor = execute_sql_query(global_db_connection, cif_insert_query, True)
                # output = cursor.fetchall()
                # execute_sql_query(global_db_connection, rdbms_update_query)
            else:
                updated_json = json.dumps(existing_json)
                # print('updated_json123',updated_json)
                rdbms_update_query = f"""UPDATE {global_database_name}.RDBMS_S3_DATA_INGESTION_CFG SET LOAD_TABLE_CFG='N',RDBMS_DB_NAME='{cfg_database_name}', RDBMS_SCHEMA_NAME='{schema_name}', RDBMS_TBL_Name='{table_name}',
                                    DataLoadTool='LF', RDBMS_TBL_PARTITIONED='{partition_key_rdbms}',
                                    AWS_TBL_PARTITIONED='{partition_flag}', RDBMS_PARTITIONED_Col='{partition_key}', RAW_TABLE='{raw_table}', S3_RAW_FULL_BUCKET_PATH='{s3_raw_full_bucket_path}',
                                    STAGE_TABLE='', S3_STAGE_FULL_BUCKET_PATH='',
                                    CURATED_TABLE='{table_name}', S3_CURATE_FULL_BUCKET_PATH='{s3_curate_full_bucket_path}', RDBMS_REFRESH_STATUS='2',
                                    RDBMS_EXEC_GROUP='{v2_execution_group}', AWS_EDS_DB='{aws_eds_db}', AWS_ACOE_DB='{aws_acoe_db}', AWS_CONA_DB='{aws_cona_db}',
                                    ONPREM_PREFIX='DT_', TIMESTAMP_PARTITION_FLAG='{v2_timestamp_partition}', encrypt_src_flag='{v2_encrypt_src_flag}', CONFIG_JSON='{updated_json}',DOMAIN_NAME='{domain_nm}',APPLICATION_NAME='{app_nm}'
                        WHERE (RDBMS_SCHEMA_NAME = '{schema_name}') and (RDBMS_TBL_Name = '{table_name}');"""
                # print("rd12",rdbms_update_query)
                rds_cur.execute(rdbms_update_query)
                # execute_sql_query(global_db_connection, rdbms_update_query)
        else:
            if partition_key == '':
                partition_flag = 'N'
            else:
                partition_flag = 'Y'
            if v2_timestamp_partition != 'Y':
                v2_timestamp_partition = 'N'
            print("v2_config_json---", v2_config_json)
            # existing_json = json.loads(v2_config_json)
            existing_json = v2_config_json
            print("existing_json", existing_json)

            existing_json["downstream"] = {"s3_path": downstream_s3_path, "handshake": downstream_handshake,
                                           "done_bucket": downstream_bucket}
            updated_json = json.dumps(existing_json)
            print("updated_json", updated_json)

            raw_table = table_name + '_raw'
            s3_raw_full_bucket_path = 's3://' + target_bucket + '/' + target_bucket_prefix + '/' + cfg_database_name + '/' + schema_name + '/' + table_name
            s3_curate_full_bucket_path = 's3://' + v2_curated_bucket + '/' + v2_curated_bucket_path
            print("s3_raw_full_bucket_path---", s3_raw_full_bucket_path)
            print("s3_curate_full_bucket_path---", s3_curate_full_bucket_path)
            print("lakeformation_flag---", lakeformation_flag)
            # s3_curate_full_bucket_path = 's3://' + v2_curated_bucket + '/' + cfg_database_name + '/' + schema_name + '/' + table_name 
            #NOTE -Use v2_curated_bucket_path instead of joining schema+table name
            #s3://cci-edo-data-curated/aws/ota_data_sets/merlin_outage/continuous_outage_fact
            if lakeformation_flag=="Y":
                tracking_columns = ['LOAD_TABLE_CFG', 'RDBMS_DB_NAME', 'RDBMS_SCHEMA_NAME', 'RDBMS_TBL_Name',
                                    'DataLoadTool', 'RDBMS_TBL_PARTITIONED',
                                    'AWS_TBL_PARTITIONED', 'RDBMS_PARTITIONED_Col', 'RAW_TABLE', 'S3_RAW_FULL_BUCKET_PATH',
                                    'STAGE_TABLE', 'S3_STAGE_FULL_BUCKET_PATH',
                                    'CURATED_TABLE', 'S3_CURATE_FULL_BUCKET_PATH', 'RDBMS_REFRESH_STATUS',
                                    'RDBMS_EXEC_GROUP', 'AWS_EDS_DB', 'AWS_ACOE_DB', 'AWS_CONA_DB',
                                    'ONPREM_PREFIX', 'TIMESTAMP_PARTITION_FLAG', 'encrypt_src_flag', 'CONFIG_JSON',
                                    'LAKEFORMATION_ENABLED_FLAG_ACOE_N', 'LAKEFORMATION_ENABLED_FLAG_CA_N',
                                    'LAKEFORMATION_ENABLED_FLAG_ACOE_SB', 'LAKEFORMATION_ENABLED_FLAG_CA', 'LAKEFORMATION_ENABLED_FLAG_ACOE','DOMAIN_NAME','APPLICATION_NAME']

                tracking_args = ["'N'", "'" + cfg_database_name + "'", "'" + schema_name + "'",
                                "'" + table_name + "'", "'LF'", "'" + partition_key_rdbms + "'",
                                "'" + partition_flag + "'", "'" + partition_key + "'",
                                "'" + raw_table + "'",
                                "'" + s3_raw_full_bucket_path + "'", "'" + "" + "'", "'" + "" + "'",
                                "'" + table_name + "'",
                                "'" + s3_curate_full_bucket_path + "'", "'2'",
                                "'" + v2_execution_group + "'",
                                "'" + aws_eds_db + "'", "'" + aws_acoe_db + "'",
                                "'" + aws_cona_db + "'",
                                "'" + "DT_" + "'", "'" + v2_timestamp_partition + "'",
                                "'" + v2_encrypt_src_flag + "'",
                                "'" + updated_json + "'","'Y'","'Y'","'Y'","'Y'","'Y'","'"+domain_nm+"'","'"+app_nm+"'"
                                ]
            else:
                tracking_columns = ['LOAD_TABLE_CFG', 'RDBMS_DB_NAME', 'RDBMS_SCHEMA_NAME', 'RDBMS_TBL_Name',
                                    'DataLoadTool', 'RDBMS_TBL_PARTITIONED',
                                    'AWS_TBL_PARTITIONED', 'RDBMS_PARTITIONED_Col', 'RAW_TABLE', 'S3_RAW_FULL_BUCKET_PATH',
                                    'STAGE_TABLE', 'S3_STAGE_FULL_BUCKET_PATH',
                                    'CURATED_TABLE', 'S3_CURATE_FULL_BUCKET_PATH', 'RDBMS_REFRESH_STATUS',
                                    'RDBMS_EXEC_GROUP', 'AWS_EDS_DB', 'AWS_ACOE_DB', 'AWS_CONA_DB',
                                    'ONPREM_PREFIX', 'TIMESTAMP_PARTITION_FLAG', 'encrypt_src_flag', 'CONFIG_JSON','DOMAIN_NAME','APPLICATION_NAME']

                tracking_args = ["'N'", "'" + cfg_database_name + "'", "'" + schema_name + "'",
                                "'" + table_name + "'", "'LF'", "'" + partition_key_rdbms + "'",
                                "'" + partition_flag + "'", "'" + partition_key + "'",
                                "'" + raw_table + "'",
                                "'" + s3_raw_full_bucket_path + "'", "'" + "" + "'", "'" + "" + "'",
                                "'" + table_name + "'",
                                "'" + s3_curate_full_bucket_path + "'", "'2'",
                                "'" + v2_execution_group + "'",
                                "'" + aws_eds_db + "'", "'" + aws_acoe_db + "'",
                                "'" + aws_cona_db + "'",
                                "'" + "DT_" + "'", "'" + v2_timestamp_partition + "'",
                                "'" + v2_encrypt_src_flag + "'",
                                "'" + updated_json + "'","'"+domain_nm+"'","'"+app_nm+"'"
                                ]

            rdbms_insert_query = 'INSERT INTO {}.{} ({}) VALUES ({})' \
                .format(global_database_name, 'RDBMS_S3_DATA_INGESTION_CFG', ', '.join(tracking_columns),
                        ', '.join(tracking_args))
            rds_cur.execute(rdbms_insert_query)
            # print("rd12345",rdbms_insert_query)
            # execute_sql_query(global_db_connection, rdbms_insert_query)
        print("inside if create_v2_metadata")
    except Exception as exception:
        print("create metadata error", str(exception))
        logger.error("Function Name: {} Error: {}".format("create_v2_metadata", str(exception)))
        # update_file_log_status(job_name, file_log_table_name, 'FAILED')
        raise Exception(str(exception))



def lambda_handler(event, context):
    # Reading global variable
    print("event, contect", event,context)
    global job_run_id, logger, rds_file_log, snowflake_rds_config_table, snowflake_procedure_name
    global df_column_header, dict_browser, dict_browser_type, dict_color_depth, dict_resolution, dict_referrer_type, dict_plugins, dict_operating_systems
    global dict_languages, dict_javascript_version, dict_event, dict_connection_type, dict_country, dict_search_engines, file_defination_nm
    global rds_conn, rds_cur

    logger = get_logger()
    print("event, contect", event,context)
    # Logging the trigger
    logger.info(f"Lambda was triggered by event:\n{event}\n\nalong with context:\n{context}")

    try:
        # Reading environment variable
        rds_secret_name = os.environ["rds_secret_name"]
        print("rds_secret_name", rds_secret_name)
        bucket = "cci-edo-data-source"
        file_dict_cif = {}
        job_run_id = get_job_id()
        v2_framework_dict = json.loads(os.environ['v2_framework'])
        # print("job_run_id, get_job_id)
        rds_file_log = os.environ["rds_file_log"]
        s3_client = boto3.client('s3')
        stage_bucket = v2_framework_dict["stage_bucket"]
        file_path = v2_framework_dict["file_path"]
        # file_path = 'cbapp'
        file_defination_nm = None
        db_details = json.loads(os.environ['DB_DETAILS'])
        app_nm = db_details['app_nm']
        domain_nm = db_details['domain_nm']
        rds_conn, rds_cur = make_rds_connection(rds_secret_name)
        print("rds_conn",rds_conn)
        print("rds_curr",rds_cur)
        # sf_conn, _, sf_dt_cur = make_snowflake_connection(snowflake_secret_name)
        file_names, full_file_paths = list_s3_objects(bucket, file_path, s3_client)
        print("file_names:--> ", file_names)
        print("full_file_paths:--> ", full_file_paths)
        file_names_paths = list(zip(file_names, full_file_paths))
        # initiate_v2_process(8043, 80845)
        s = None
        file_defination_nm_list = []
        file_gz = ''
        file_gz_pth = ''
        chk = 0
        for file_name, key in file_names_paths:
            print("file_names:-->1234 ", file_name)
            file_defination_nm = file_name
            if '.tsv.gz' in file_name and not '.tar.gz' in file_name:
                file_gz = file_name
                file_gz_pth = key
                file_defination_nm = file_name.replace('.gz', '')
                file_defination_nm_list.append(file_defination_nm)
                print("file_defination_nm-----==== here", file_defination_nm)
                # continue
            elif 'browser.tsv' in file_name or 'browser_type.tsv'  in file_name or 'color_depth.tsv'  in file_name \
            or 'column_headers.tsv'  in file_name or 'connection_type.tsv'  in file_name or 'country.tsv'  in file_name \
            or 'event.tsv' in file_name or 'javascript_version.tsv' in file_name or 'languages.tsv' in file_name or 'operating_systems.tsv' in file_name or 'plugins.tsv'  in file_name  \
            or 'referrer_type.tsv'  in file_name or 'resolution.tsv'  in file_name or 'search_engines.tsv' or not file_name.endswith('.txt') or not file_name.endswith('.tar.gz'):
                file_defination_nm = file_name   
                file_defination_nm_list.append(file_defination_nm)
                print("file_defination_nm-----==== there", file_defination_nm)
                # continue
            elif file_name.endswith('.txt'):
                # file_names.remove(file_name)
                continue
            elif '.tsv' in file_name and not '.tsv.gz' in file_name:
                print("tsv file", file_name)
                file_defination_nm = file_name
                file_defination_nm_list.append(file_defination_nm)
                print("file_defination_nm-----==== tthere", file_defination_nm)
            print("file_defination_nm-----====", file_defination_nm)
            print("file_defination_nm_list-->111", file_defination_nm_list)
            #check for existing file processed or not
            chk = check_file_processed(rds_cur, file_defination_nm, 'COMPLETED')
            print("chk", chk, file_name, file_defination_nm)
            if chk>=1 and chk <10:
                print("file already processed---->", file_defination_nm)
                print("file_names present---->", file_name)
                print("full_file_paths present---->", key)
                print("full_file_paths file_names---->", file_names)
                print("full_file_paths full_file_paths---->", full_file_paths)
                for file_nm in file_names:
                    if file_defination_nm in file_nm:
                        print("1",file_nm, file_names.index(file_nm))
                        full_file_paths.pop(file_names.index(file_nm))
                        print("full_file_paths file_names---12->", file_names)
                        file_names.pop(file_names.index(file_nm))
                        print("2")
                file_defination_nm_list = list(filter(lambda x: x != file_defination_nm, file_defination_nm_list))
            elif chk >10:
                chk = check_file_processed(rds_cur, file_defination_nm, 'FAILED')
                print("checking more times", chk, file_defination_nm)
                # sys.exit(1)
                print("file_namesss", file_names)
                print("full_file_pathsss", full_file_paths)
                file_defination_nm_list = list(filter(lambda x: x != file_defination_nm, file_defination_nm_list))
                print("file already file_defination_nm_list---->", file_defination_nm_list)
                # file_defination_nm_list.remove(file_defination_nm)
                s = 'ALREADY PROCESSED'
            # else:
        print("file_names_paths previous---->", file_names_paths, len(file_names_paths))
        file_names_paths = list(zip(file_names, full_file_paths))
        print("file_names_paths after---->", file_names_paths,len(file_names_paths))
        print("file_defination_nm_list-->", file_defination_nm_list)
        file_defination_nm_list = list(set(file_defination_nm_list))
        print("file_defination_nm_list--set-->", file_defination_nm_list)
        # Insert FILE_LOG entry
        print("job_run_id", job_run_id)
        job_id_list = {}
        if len(file_defination_nm_list) == 1 and 'column_headers.tsv' in file_defination_nm_list:
            s = 'No file'
            file_defination_nm = file_defination_nm_list[0]
            print("no file left")
            rds_conn.close()
            sys.exit(1)
        if len(file_defination_nm_list) == 2 and 'column_headers.tsv' in file_defination_nm_list and 'coxnew-cbma-mobile-prod_2023-11-01-lookup_data.tar.gz' in file_defination_nm_list:
            s = 'No file'
            file_defination_nm = file_defination_nm_list[0]
            print("no file left")
            rds_conn.close()
            sys.exit(1)
        if file_defination_nm_list:
            print("file_defination_nm_list-->123", file_defination_nm_list)
            for fnm in file_defination_nm_list:
                job_run_id = get_job_id()
                job_id = insert_file_log(rds_cur,fnm, job_run_id)
                job_id_list[fnm] = job_id
                print("job_run_id1236", job_id, fnm)
                table_nm = fnm
                if 'browser.tsv' in fnm or 'browser_type.tsv'  in fnm or 'color_depth.tsv'  in fnm \
                or 'column_headers.tsv'  in fnm or 'connection_type.tsv'  in fnm or 'country.tsv'  in fnm \
                or 'event.tsv' in fnm or 'javascript_version.tsv' in fnm or 'languages.tsv' in fnm or 'operating_systems.tsv' in fnm or 'plugins.tsv'  in fnm  \
                or 'referrer_type.tsv'  in fnm or 'resolution.tsv'  in fnm or 'search_engines.tsv' in fnm:
                    print("job_run_id1236311", job_id, fnm)
                    # pass
                else:
                    print("job_run_id12363", job_id, fnm)
                    cif_id = insert_cif_job_status_record(rds_cur, fnm, 'CBAPP_BASE')
                    file_dict_cif[fnm] = cif_id
                    
              
            print("file_dict_cif--->", file_dict_cif)
            print("job_id_list--->", job_id_list)
            # unzip_file(rds_cur)
            # raise Exception("testing")
            s, file_defination_nm , file_defination_df= unzip_file(rds_cur, file_names, full_file_paths, file_dict_cif, job_id_list)
            print("file_defination_nm------------===>", file_defination_nm)
            print("file_defination_nm------------===>", file_defination_df)
            for fnm in file_defination_df:
                cif_id = file_defination_df.get(fnm)
                # dfcnt = file_dict_count.get(fnm)
                print("cifid-----", cif_id)
                update_cif_job_status_record(rds_cur,cif_id, '', '', fnm, 'N')
                
            # update_file_log(rds_cur, "COMPLETED", "COMPLETED", "FILE PROCESSED", file_defination_nm)
        
        print("File process complete",file_defination_nm_list)
        print("File process status",s)
        if  s=='COMPLETED' :
            payload_data = {
                'process_name': 'aws_daily_automatic_cbapp'
            }
            lambda_client = boto3.client('lambda')
            # payload['process_name'] = 'aws_daily_automatic_cbapp'
            payload_str = json.dumps(payload_data)
    
            try:
                # Invoke the Lambda function
                response = lambda_client.invoke(
                    FunctionName='lambda_trigger_data_transform_framework_cf',
                    InvocationType='RequestResponse',  # Use 'Event' for asynchronous invocation
                    Payload=payload_str,  # Convert payload to string format
                )
                
                # Parse and return the response
                print("response['Payload'].read().decode('utf-8')", response['Payload'].read().decode('utf-8'))
                return response['Payload'].read().decode('utf-8')
            
            except Exception as e:
                print(f"Error invoking Lambda function lambda_trigger_data_transform_framework_cf: {e}")
                # return None
        rds_conn.close()
        sys.exit(1)
        return "Ok"

    except Exception as e:
        print("error in lambda handler function",str(e))
        logger.error(f"Error encountered in lambda_handler function.\nError: {str(e)}")
        # rds_conn.close()
        sys.exit(1)
        
