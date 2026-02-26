from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'spark_cassandra_bikes_dag',
    default_args=default_args,
    description='Recoge datos de bicis y los almacena en Cassandra',
    schedule_interval='*/2 * * * *',  # Cada 2 minutos
    catchup=False,
)

run_etl_script = BashOperator(
    task_id='run_spark_bike_job',
    bash_command='python3 /opt/airflow/scripts/spark_cassandra_bikes.py',
    dag=dag,
)
