import airflow
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pendulum
import sys
from modules.S32SNF import main
import time

sys.path.append("$AIRFLOW_HOME/modules/")

local_tz = pendulum.timezone("US/Eastern")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 27, tzinfo=local_tz),
    "retries": 1
}

dag = DAG(
    dag_id="CA_EDW_COMM_PROD_CODE_DAILY_FACT_INCREMENTAL_DI_LOAD",
    schedule_interval='@once',
    default_args=default_args,
    catchup=False
)


def CALLini_function(**kwargs):
    job_nm = kwargs["templates_dict"]["job_nm"]
    source_table = kwargs["templates_dict"]["source_table"]
    target_table = kwargs["templates_dict"]["target_table"]
    return main(ingestion_type="INCREMENTAL_LOAD", job_nm=job_nm, source_table=source_table, target_table=target_table)

def wait():
    time.sleep(1*60)

# START & END TASK
START = DummyOperator(task_id="START", default_args=default_args, dag=dag)
END = DummyOperator(task_id="END", default_args=default_args, dag=dag)
WAIT = PythonOperator(task_id='WAIT', python_callable=wait, default_args=default_args, dag=dag)


# COMM_PROD_CODE_DAILY_FACT
TEMP_COMM_PROD_CODE_DAILY_FACT = PythonOperator(task_id='TEMP_COMM_PROD_CODE_DAILY_FACT', templates_dict={"job_nm": "CA_EDW_COMM_PROD_CODE_DAILY_FACT_INCREMENTAL_DI_LOAD_TEMP_COMM_PROD_CODE_DAILY_FACT",'source_table': 'STRM_COMM_PROD_CODE_DAILY_FACT', 'target_table': 'TEMP_COMM_PROD_CODE_DAILY_FACT'}, python_callable=CALLini_function, default_args=default_args, dag=dag)
AUDIT_COMM_PROD_CODE_DAILY_FACT = PythonOperator(task_id='AUDIT_COMM_PROD_CODE_DAILY_FACT', templates_dict={"job_nm": "CA_EDW_COMM_PROD_CODE_DAILY_FACT_INCREMENTAL_DI_LOAD_AUDIT_COMM_PROD_CODE_DAILY_FACT",'source_table': 'TEMP_COMM_PROD_CODE_DAILY_FACT', 'target_table': 'AUDIT_IRS_TABLES'}, python_callable=CALLini_function, default_args=default_args, dag=dag)
DELETE_COMM_PROD_CODE_DAILY_FACT = PythonOperator(task_id='DELETE_COMM_PROD_CODE_DAILY_FACT', templates_dict={"job_nm": "CA_EDW_COMM_PROD_CODE_DAILY_FACT_INCREMENTAL_DI_LOAD_DELETE_COMM_PROD_CODE_DAILY_FACT",'source_table': 'TEMP_COMM_PROD_CODE_DAILY_FACT', 'target_table': 'COMM_PROD_CODE_DAILY_FACT'}, python_callable=CALLini_function, default_args=default_args, dag=dag)
COMM_PROD_CODE_DAILY_FACT = PythonOperator(task_id='COMM_PROD_CODE_DAILY_FACT', templates_dict={"job_nm": "CA_EDW_COMM_PROD_CODE_DAILY_FACT_INCREMENTAL_DI_LOAD_COMM_PROD_CODE_DAILY_FACT",'source_table': 'TEMP_COMM_PROD_CODE_DAILY_FACT', 'target_table': 'COMM_PROD_CODE_DAILY_FACT'}, python_callable=CALLini_function, default_args=default_args, dag=dag)




START >> WAIT >> TEMP_COMM_PROD_CODE_DAILY_FACT >> AUDIT_COMM_PROD_CODE_DAILY_FACT >> DELETE_COMM_PROD_CODE_DAILY_FACT >> COMM_PROD_CODE_DAILY_FACT >> END