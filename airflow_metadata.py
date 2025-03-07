# Importing necessary libraries
import pandas as pd
from airflow.decorators import dag, task
from airflow.models import DagModel, DagRun, TaskFail, TaskInstance, Variable, Connection, XCom, SlaMiss
from airflow.utils.dates import days_ago
from airflow.utils.session import create_session
from datetime import datetime
import logging
import boto3
from sqlalchemy import inspect
from io import StringIO

# Constants
METADATA_LOOKBACK_DAYS = 10  # Lookback period in days for filtering metadata

# Airflow models to export and their associated date fields for filtering
MODELS_TO_EXPORT = [
    {"model": DagModel, "date_field": None},
    {"model": Variable, "date_field": None},
    {"model": DagRun, "date_field": DagRun.execution_date},
    {"model": TaskInstance, "date_field": TaskInstance.execution_date},
    {"model": TaskFail, "date_field": TaskFail.start_date},
    # {"model": dg, "date_field": dg.start_date},
    {"model": Connection, "date_field": None},
    {"model": XCom, "date_field": XCom.execution_date},
    {"model": SlaMiss, "date_field": None},
]

S3_BUCKET = "cci-edo-data-utils"
S3_PREFIX = "airflow-sb/dags/airflow_metadata_informations/"

def export_to_s3(data_frame, table_name):
    s3 = boto3.client("s3")
    csv_buffer = StringIO()
    data_frame.to_csv(csv_buffer, index=False)
    s3_key = f"{S3_PREFIX}{table_name}.csv"

    try:
        s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=csv_buffer.getvalue())
        logging.info(f"Data successfully exported to S3: s3://{S3_BUCKET}/{s3_key}")
    except Exception as e:
        logging.error(f"Error exporting data to S3: {e}")

DEFAULT_DAG_ID = "airflow_metadata_dag1"
DEFAULT_TASK1_ID = "extract_metadata1"
DEFAULT_TASK2_ID = "log_completion1"


@dag(
    dag_id=DEFAULT_DAG_ID,
    schedule="@daily",
    start_date=datetime(2021, 12, 1),
    catchup=False,
    default_args={"owner": "airflow"},
)



def metadata_extraction_dag():

    @task(task_id=DEFAULT_TASK1_ID)
    def extract_metadata():
        with create_session() as session:
            # Get the underlying engine (database connection)
            engine = session.bind
            # Get the current connection details
            connection = engine.connect()

            # Log the engine details (e.g., the database URL)
            logging.info(f"Database URL: {engine.url}")
            
            # Log the connection details (e.g., the database connection type)
            logging.info(f"Connection Details: {connection.info}")
            
            # If you want to inspect the engine's dialect (database type)
            dialect = engine.dialect
            logging.info(f"Dialect: {dialect.name}")
            inspector = inspect(engine)  # Create an Inspector for exploring the database

            # List all schemas in the database
            schemas = inspector.get_schema_names()
            print(f"Schemas: {schemas}")

            # List all tables in the public schema (you can specify a schema name as well)
            tables = inspector.get_table_names(schema='public')  # Specify schema if needed
            print(f"Tables in 'public' schema: {tables}")

            # Optionally, print details about columns in a specific table
            for table_name in tables:
                columns = inspector.get_columns(table_name, schema='public')
                print(f"Columns in table {table_name}: {columns}")
                
            # List all tables in the public schema (you can specify a schema name as well)
            tables1 = inspector.get_table_names(schema='information_schema')  # Specify schema if needed
            print(f"Tables in 'information_schema' schema: {tables1}")

            # Optionally, print details about columns in a specific table
            for table_name in tables1:
                columns = inspector.get_columns(table_name, schema='information_schema')
                print(f"Columns in table {table_name} 'information_schema' schema: {columns}")
            
            for entry in MODELS_TO_EXPORT:
                model = entry["model"]
                date_field = entry["date_field"]
                rows_list = []

                if date_field:
                    query = session.query(model).filter(date_field >= days_ago(METADATA_LOOKBACK_DAYS))
                else:
                    query = session.query(model)

                rows = query.all()
                table_name = model.__name__.upper()
                logging.info(f"Processing table: {table_name}")

                if rows:
                    for row in rows:
                        rows_list.append(vars(row))

                    data_frame = pd.DataFrame(rows_list)
                    data_frame.columns = map(str.upper, data_frame.columns)
                    data_frame = data_frame.astype(str, errors="ignore")
                    # print(f"++++++++++++++++++++++++Printing Data Frame Start++++++++++++++++++++++++")
                    # print(data_frame)
                    # print(f"++++++++++++++++++++++++Printing Data Frame End++++++++++++++++++++++++")
                    logging.info(f"Extracted columns are {data_frame.columns}")
                    if 'DAG_ID' in data_frame.columns:
                        logging.info(f"Extracted dagid are {data_frame['DAG_ID']}")
                    logging.info(f"Extracted data from {table_name}")
                    logging.info(f"Extracted data from {data_frame.head()}")
                    export_to_s3(data_frame, table_name)
                    logging.info(f"Extracted data to s3 ")
                else:
                    logging.info(f"No data found for table: {table_name}")

    @task(task_id=DEFAULT_TASK2_ID)
    def log_completion():
        logging.info("Metadata extraction process completed successfully.")

    # @task(task_id=DEFAULT_TASK3_ID)
    # def export_to_s3(data_frame, table_name):
    #     S3_BUCKET = "cci-edo-data-utils"
    #     S3_PREFIX = "airflow-sb/dags/airflow_metadata_informations/"
    #     s3 = boto3.client("s3")
    #     csv_buffer = StringIO()
    #     data_frame.to_csv(csv_buffer, index=False)
    #     s3_key = f"{S3_PREFIX}{table_name}.csv"
        
    #     try:
    #         s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=csv_buffer.getvalue())
    #         logging.info(f"Data successfully exported to S3: s3://{S3_BUCKET}/{s3_key}")
    #     except Exception as e:
    #         logging.error(f"Error exporting data to S3: {e}")

    # metadata, table_name = extract_metadata()  # Extract metadata
    # export_to_s3(metadata, table_name)  # Export to S3
    # log_completion()

    # extract_metadata() >> log_completion() >> export_to_s3(metadata, table_name)
    extract_metadata() >> log_completion()

metadata_extraction_dag()