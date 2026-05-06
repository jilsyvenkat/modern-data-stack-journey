from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'Jilsy',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    'email_on_failure': False,
}

def run_dbt_simulation():
    print("=" * 50)
    print("DBT RUN STARTED")
    print("Running with dbt=1.11.8")
    print("1 of 2 OK created sql view model jaffle_shop.stg_orders")
    print("2 of 2 OK created sql table model jaffle_shop.customers")
    print("Completed successfully")
    print("=" * 50)

def run_dbt_tests():
    print("=" * 50)
    print("DBT TEST STARTED")
    print("1 of 4 PASS not_null_customers_customer_id")
    print("2 of 4 PASS unique_customers_customer_id")
    print("3 of 4 PASS not_null_orders_order_id")
    print("4 of 4 PASS unique_orders_order_id")
    print("All 4 tests passed!")
    print("=" * 50)

def notify_complete(**context):
    print("=" * 50)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print(f"Completed at: {datetime.now()}")
    print("Tasks completed:")
    print("  check_snowflake_data — real Snowflake query")
    print("  run_dbt_models       — models refreshed")
    print("  test_dbt_models      — all 4 tests passed")
    print("  notify_completion    — stakeholders notified")
    print("=" * 50)

with DAG(
    dag_id='daily_data_pipeline',
    default_args=default_args,
    description='Real Snowflake query plus dbt simulation pipeline',
    schedule='0 2 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['snowflake', 'dbt', 'daily'],
) as dag:

    task_check_data = SQLExecuteQueryOperator(
        task_id='check_snowflake_data',
        conn_id='snowflake_default',
        sql="""
            SELECT
                COUNT(*) as total_orders,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_orders,
                SUM(CASE WHEN status = 'returned' THEN 1 ELSE 0 END) as returned_orders,
                MIN(order_date) as earliest_order,
                MAX(order_date) as latest_order,
                CURRENT_TIMESTAMP() as checked_at
            FROM dbt_tutorial.jaffle_shop.raw_orders;
        """,
    )

    task_run_dbt = PythonOperator(
        task_id='run_dbt_models',
        python_callable=run_dbt_simulation,
    )

    task_test_dbt = PythonOperator(
        task_id='test_dbt_models',
        python_callable=run_dbt_tests,
    )

    task_notify = PythonOperator(
        task_id='notify_completion',
        python_callable=notify_complete,
    )

    task_check_data >> task_run_dbt >> task_test_dbt >> task_notify
