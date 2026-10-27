from datetime import datetime, timedelta
import os, subprocess, sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
with DAG(dag_id='zomato_local_elt', description='Ingest CSVs then build dbt models and tests', start_date=datetime(2025,1,1), schedule=None, catchup=False, default_args={'owner':'data-engineering','retries':2,'retry_delay':timedelta(minutes=2)}, tags=['zomato','local']) as dag:
    def ingest():
        env=os.environ.copy(); env['ZOMATO_DATA_DIR']='/opt/data'
        subprocess.run([sys.executable,'/opt/ingestion/load_csv.py'],check=True,env=env)
    load=PythonOperator(task_id='ingest_csv_to_raw',python_callable=ingest)
    build=BashOperator(task_id='dbt_build_and_test',bash_command='cd /opt/dbt/project && dbt build --profiles-dir /opt/dbt --target local')
    load >> build
