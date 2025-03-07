# *********************** DEV NOTE *************************************************************************************
# AUTHOR: SUMEET AGARWAL
# VERSION: 2
# BUILD DATE: 05/06/2023
# FRAMEWORK: SNOWFLAKE DAGS EVENT TRIGGER
# PROCESS NAME: CCI_EDS_LAMBDA_SNOWFLAKE_DAGS_EVENT_TRIGGER_CF
# FUNCTIONALITY: This process is used to Trigger AWS MWAA DAGs based on S3 Event Notifications.
# DO NOT EDIT OR TINKER!!!!!
# INVOCATIONS : AD-HOC
# **********************************************************************************************************************


import ast
import base64
import boto3
import http.client
import json
import logging
import os
import pymysql
import uuid


global logger
global rds_log_table_name
global cursor
global file_description


def get_logger():
    """
    This function is used to create a logger object.
    """

    # Declaring standard format variables
    logging_format = "%(asctime)s %(levelname)s %(name)s:\t%(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Setting configuration ar per our need
    logging.basicConfig(format=logging_format, datefmt=date_format)
    temp_logger = logging.getLogger("CCI_EDS_LAMBDA_SNOWFLAKE_DAGS_EVENT_TRIGGER_CF")
    temp_logger.setLevel(logging.INFO)

    return temp_logger


def get_secret():
    """
    This functions retrieves the information from Secret Manager for connecting to RDS.
    :return: Information to connect to RDS.
    """

    try:
        logger.info("Inside get_secret function. Process started to retrieve secrets from secret manager.")

        secret_name = os.environ["rds_secret_name"]
        region_name = "us-east-1"
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = eval(get_secret_value_response["SecretString"])

        endpoint = secret["host"]
        dbuser = secret["username"]
        password = secret["password"]
        port = secret["port"]
        database = secret["dbname"]
        logger.info("Inside get_secret function. Process completed to retrieve secrets from secret manager.")

        return endpoint, dbuser, password, int(port), database

    except Exception as e:
        logger.exception(f"Error encountered in get_secret function.\nError: {str(e)}.")


def get_file_description():
    """
    This function is used to generate UUID.
    :return: Python String.
    """

    return str(uuid.uuid4())


def insert_file_log():
    """
    This function is used to insert entry into RDS Log Table.
    :return: None.
    """

    try:

        logger.info("Inside insert_file_log function. Process started to insert an entry.")

        # Inserting an entry
        cursor.execute(f"INSERT INTO {rds_log_table_name} (file_definition_id, file_process_status, "
                       f"file_dt, create_dt, last_update_dt, stage, file_description) "
                       f"VALUES('EVENT_DAG_TRIGGER', 'STARTED', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), "
                       f"CURRENT_TIMESTAMP(), 'STARTED', '{file_description}');")

        logger.info("Inside insert_file_log function. Process completed to insert an entry.")

    except Exception as e:
        logger.exception(f"Error encountered in insert_file_log function.\nError: {str(e)}")


def update_file_log(dag_name, process_status, serial_number, error_msg, stage):
    """
    This function is used to update entry into RDS Log Table.
    :param dag_name: Python String representing the AWS MWAA DAG Name.
    :param process_status: Python String representing the process status.
    :param serial_number: Python Integer representing the AWS MWAA DAG RDS serial number
    :param error_msg: Python String representing the error message.
    :param stage: Python String representing the stage status.
    :return: None.
    """

    try:

        logger.info("Inside update_file_log function. Process started to update an entry.")

        # Inserting an entry
        cursor.execute(f"UPDATE {rds_log_table_name} SET file_definition_nm='{dag_name}', "
                       f"file_process_status='{process_status}', last_update_dt=CURRENT_TIMESTAMP(), "
                       f"JOB_ID='{serial_number}', error_msg='{error_msg}', stage='{stage}' "
                       f"WHERE file_definition_id='EVENT_DAG_TRIGGER' "
                       f"AND file_description='{file_description}';")

        logger.info("Inside update_file_log function. Process completed to update an entry.")

    except Exception as e:
        logger.exception(f"Error encountered in update_file_log function.\nError: {str(e)}")


def get_dictionary_key_value(python_dict, key):
    """
    This function is used to get the value of Python Dictionary's Key.
    The search is Case-Insensitive.
    :param python_dict: Python Dictionary representing the Dictionary we want to parse.
    :param key: Python String representing the Key we want to find.
    :return: Python String representing the Value of corresponding Key in Dictionary.
    """

    try:

        logger.info("Inside get_dictionary_key_value function. Process started to fetch key value.")
        update_file_log("", "IN PROGRESS", "", "", "EXTRACTING KEY VALUE STARTED.")

        key_list = python_dict.keys()
        for i in key_list:
            if key.lower() == i.lower():
                logger.info("Inside get_dictionary_key_value function. Process completed to fetch key value.")
                update_file_log("", "IN PROGRESS", "", "", "EXTRACTING KEY VALUE COMPLETED.")
                return python_dict[i]

        logger.error("Inside get_dictionary_key_value function. Process failed to fetch key value.")
        update_file_log("", "FAILED", "", "KEY NOT FOUND.", "EXTRACTING KEY VALUE FAILED.")
        return None

    except Exception as e:
        logger.exception(f"Error encountered in get_dictionary_key_value function.\nError: {str(e)}")
        error_msg = str(e).replace("'", '"')
        update_file_log("", "FAILED", "", error_msg, "EXTRACTING KEY VALUE FAILED.")


def get_s3_key_list(s3_bucket_name, s3_prefix):
    """
    This function is used to get list of all possible table paths.
    :param s3_bucket_name: Name of bucket in which file event was received.
    :param s3_prefix: S3 prefix/key of the file for which event was received.
    :return: Python List of all possible table paths.
    """

    try:
        logger.info("Inside get_s3_key_list function. Process started to generate S3 paths.")

        # Declaring an empty list
        final_list = []

        # Creating the original S3 prefix along with bucket
        original_path = s3_bucket_name + "/" + s3_prefix
        temp_list = original_path.split("/")

        for i in range(2, len(temp_list) + 1):
            final_list.append(temp_list[0] + "/" + "/".join(temp_list[1:i]))

        final_list.reverse()
        logger.info("Inside get_s3_key_list function. Process completed to generate S3 paths.")
        return final_list

    except Exception as e:
        logger.exception(f"Error encountered in get_s3_key_list function.\nError: {str(e)}")


def get_dag_name(list_of_table_path):
    """
    This function is used to get corresponding DAG name from RDS lookup table.
    :param list_of_table_path: Python List of all possible table paths.
    :return: Python List containing RDA Serial Number and AWS MWAA DAG name.
    """

    try:

        logger.info("Inside get_dag_name function. Process started to determine the DAG to be triggered.")
        update_file_log("", "IN PROGRESS", "", "", "RETRIEVING DAG INFORMATION STARTED.")

        # Declaring python variable to store DAG name
        dag_name = None
        serial_no = None

        # Retrieving information for RDS table
        rds_dag_info_table_name = os.environ["rds_dag_info_table_name"]

        # Iterating over the table path
        # Preparing SQL and checking if we get DAG name
        for path in list_of_table_path:
            if not dag_name and not serial_no:
                sql_query = f"SELECT SERIAL_NO , dag_name FROM {rds_dag_info_table_name} WHERE table_path = '{path}';"
                cursor.execute(sql_query)
                result = cursor.fetchall()
                if len(result) != 0:
                    dag_name = result[0][1]
                    serial_no = result[0][0]
                    logger.info("Successfully found corresponding DAG.")
                    logger.info("Inside get_dag_name function. Process started to determine the DAG to be triggered.")
                    update_file_log(dag_name, "IN PROGRESS", serial_no, "", "RETRIEVING DAG INFORMATION COMPLETED.")
                    return [serial_no, dag_name]

        logger.error("Inside get_dag_name function. Process completed to determine the DAG to be triggered.")
        update_file_log("", "FAILED", "", "NO DAG INFORMATION FOUND.", "RETRIEVING DAG INFORMATION FAILED.")
        return []

    except Exception as e:
        logger.exception(f"Error encountered in get_dag_name function.\nError: {str(e)}")
        error_msg = str(e).replace("'", '"')
        update_file_log("", "FAILED", "", error_msg, "RETRIEVING DAG INFORMATION FAILED.")


def trigger_mwaa_dag(serial_no, dag_name):
    """
    This function is used to trigger an AWS MWAA DAG.
    :param serial_no: Python Integer representing the RDS Serial Number.
    :param dag_name: Python String representing the DAG name to be triggered.
    :return: None.
    """

    try:

        logger.info("Inside trigger_mwaa_dag function. Process started to trigger a DAG.")
        update_file_log(dag_name, "IN PROGRESS", serial_no, "", "TRIGGER DAG STARTED.")

        # Triggering a DAG
        mwaa_env_name = os.environ["mwaa_env_name"]
        mwaa_client = boto3.client("mwaa")
        mwaa_cli_token = mwaa_client.create_cli_token(Name=mwaa_env_name)
        conn = http.client.HTTPSConnection(mwaa_cli_token["WebServerHostname"])
        payload = "dags trigger " + dag_name
        headers = {"Authorization": "Bearer " + mwaa_cli_token["CliToken"], "Content-Type": "text/plain"}
        conn.request("POST", "/aws_mwaa/cli", payload, headers)
        res = conn.getresponse()
        logger.info(f"DAG {dag_name} successfully triggered.")
        logger.info(base64.b64decode(ast.literal_eval(res.read().decode("UTF-8"))["stdout"]))
        logger.info("Inside trigger_mwaa_dag function. Process completed to trigger a DAG.")
        update_file_log(dag_name, "IN PROGRESS", serial_no, "", "TRIGGER DAG COMPLETED.")

    except Exception as e:
        logger.exception(f"Error encountered in trigger_mwaa_dag function.\n Error: {str(e)}")
        error_msg = str(e).replace("'", '"')
        update_file_log(dag_name, "FAILED", serial_no, error_msg, "TRIGGER DAG FAILED.")


def sqs_process_flow(msg):
    """
    This function is used to trigger AWS MWAA DAGs for SQS received messages.
    :param msg: Python Dictionary Representing the message received from SQS.
    :return: None.
    """

    try:
        logger.info("Inside sqs_process_flow function. Process started for SQS.")
        update_file_log("", "IN PROGRESS", "", "", "SQS PROCESS STARTED.")

        # Extracting the S3 Bucket name and key from Event
        # For example: cci-cdo-data-curated/cmi/report-reference-data/billcycle/dt=2022-05-02/CMI_BILLCYCLE_DIM.parquet
        # Bucket-name : cci-cdo-data-curated
        # Key : cmi/report-reference-data/billcycle_dim/dt=2022-05-02/CMI_BILLCYCLE_DIM.parquet
        for item in msg["Records"]:
            s3_bucket = json.loads(json.loads(item["body"])["Message"])["Records"][0]["s3"]["bucket"]["name"]
            s3_key = json.loads(json.loads(item["body"])["Message"])["Records"][0]["s3"]["object"]["key"]
            table_path_list = get_s3_key_list(s3_bucket, s3_key)
            logger.info("Processing of Event information completed.")
            logger.info("Inside sqs_process_flow function. Process completed for SQS.")
            update_file_log("", "IN PROGRESS", "", "", "SQS PROCESS COMPLETED.")
            return table_path_list

    except Exception as e:
        logger.exception(f"Error encountered in sqs_process_flow function.\nError: {str(e)}")
        error_msg = str(e).replace("'", '"')
        update_file_log("", "FAILED", "", error_msg, "SQS PROCESS FAILED.")


def sns_process_flow(msg):
    """
    This function is used to trigger AWS MWAA DAGs for SQS received messages.
    :param msg: Python Dictionary Representing the message received from SQS.
    :return: None.
    """

    try:
        logger.info("Inside sns_process_flow function. Process started for SNS.")
        update_file_log("", "IN PROGRESS", "", "", "SNS PROCESS STARTED.")

        # Extracting the information from Event
        schema_name = msg["Records"][0]["Sns"]["MessageAttributes"]["Schema"]["Value"]
        table_name = msg["Records"][0]["Sns"]["MessageAttributes"]["Table"]["Value"]
        logger.info("Processing of Event information completed.")
        logger.info("Inside sns_process_flow function. Process completed for SNS.")
        update_file_log("", "IN PROGRESS", "", "", "SNS PROCESS COMPLETED.")
        return [f"{schema_name}/{table_name}"]

    except Exception as e:
        logger.exception(f"Error encountered in sns_process_flow function.\nError: {str(e)}")
        error_msg = str(e).replace("'", '"')
        update_file_log("", "FAILED", "", error_msg, "SNS PROCESS FAILED.")


def lambda_handler(event, context):
    """
    This is the main execution point for our Lambda.
    Whenever Lambda is triggered or invoked the execution starts from this function.
    :param event: The event type and information that is invoking the Lambda to execute.
    :param context: Additional information passed along with event at time of invoking.
    :return: Triggers a DAG based on the event.
    """

    # Reading global variables
    global cursor, logger, rds_log_table_name, file_description

    try:

        # Initializing variables
        logger = get_logger()
        rds_log_table_name = os.environ["rds_log_table_name"]
        file_description = get_file_description()

        # Logging the event
        logger.info(f"Lambda  was triggered for event:- \n{event}")
        logger.info(f"Lambda  was triggered for context:- \n{context}")

        # Establishing connection with RDS
        endpoint, dbuser, password, port, database = get_secret()
        conn = pymysql.connect(
            host=endpoint,
            user=dbuser,
            passwd=password,
            port=port,
            autocommit=True
        )
        cursor = conn.cursor()

        # Inserting into RDS Log table
        insert_file_log()

    except Exception as e:
        logger.exception(f"Error encountered in lambda_handler function.\nError: {str(e)}")

    try:

        # Initializing variables
        table_path_list = None

        # Determining the invocation
        invoker_type = get_dictionary_key_value(event["Records"][0], "EventSource")
        if invoker_type is not None:
            logger.info(f"invoker_type: {invoker_type}")

            if invoker_type.lower() == "aws:sqs".lower():
                table_path_list = sqs_process_flow(event)
            elif invoker_type.lower() == "aws:sns".lower():
                table_path_list = sns_process_flow(event)

            if table_path_list is not None:
                result = get_dag_name(table_path_list)

                if len(result) != 0:
                    serial_no, dag_name = result
                    logger.info(f"DAG Found at serial number: {serial_no} with '{dag_name}' name.")
                    update_file_log(
                        dag_name,
                        "IN PROGRESS",
                        serial_no,
                        "",
                        "TRIGGERING DAG IN PROGRESS."
                    )
                    trigger_mwaa_dag(serial_no, dag_name)

                    cursor.execute(f"UPDATE {rds_log_table_name} SET file_process_status='COMPLETED', "
                                   f"last_update_dt=CURRENT_TIMESTAMP(), stage='COMPLETED' "
                                   f"WHERE file_definition_id='EVENT_DAG_TRIGGER' "
                                   f"AND file_description='{file_description}';")

                else:
                    logger.info(f"No DAG Found for table path: '{table_path_list}'.")
                    cursor.execute(f"UPDATE {rds_log_table_name} SET file_process_status='COMPLETED', "
                                   f"last_update_dt=CURRENT_TIMESTAMP(), error_msg='NO CORRESPONDING DAG FOUND.', "
                                   f"stage='PARTIALLY COMPLETED' WHERE file_definition_id='EVENT_DAG_TRIGGER' "
                                   f"AND file_description='{file_description}';")
            else:
                logger.error("Inside lambda_handler function. Process failed due to invalid invoker.")
                update_file_log("", "FAILED", "", "INVALID INVOCATION RECEIVED FROM UNKNOWN INVOKER.", "FAILED.")

    except Exception as e:
        logger.exception(f"Error encountered in lambda_handler function.\nError: {str(e)}")
        update_file_log("", "FAILED", "", "INVALID INVOCATION RECEIVED FROM UNKNOWN INVOKER.", "FAILED.")
