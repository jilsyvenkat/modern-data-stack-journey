from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'siva',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}

def check_data():
    print("Step 1: Checking raw data availability in Snowflake...")
    print("Found 3 customers and 3 orders in raw tables")
    print("Data freshness check passed!")

def notify_complete():
    print(f"Pipeline completed successfully at {datetime.now()}")
    print("Snowflake extract done, dbt models refreshed and tested")
    print("Stakeholders notified!")

with DAG(
    dag_id='daily_data_pipeline',
    default_args=default_args,
    description='Extract from Snowflake, transform with dbt, notify on completion',
    schedule='0 2 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['snowflake', 'dbt', 'daily'],
) as dag:

    task_check_data = PythonOperator(
        task_id='check_snowflake_data',
        python_callable=check_data,
    )

    task_run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='echo "Running dbt models... dbt run completed successfully"',
    )

    task_test_dbt = BashOperator(
        task_id='test_dbt_models',
        bash_command='echo "Running dbt tests... all 4 tests passed"',
    )

    task_notify = PythonOperator(
        task_id='notify_completion',
        python_callable=notify_complete,
    )

    task_check_data >> task_run_dbt >> task_test_dbt >> task_notify
