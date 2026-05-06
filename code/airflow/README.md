# Airflow DAG — daily_data_pipeline

## What this DAG does
A 4-task pipeline demonstrating Airflow orchestration with a
real Snowflake connection.

## Task flow
\```
check_snowflake_data → run_dbt_models → test_dbt_models → notify_completion
SQLExecuteQueryOp      PythonOperator   PythonOperator    PythonOperator
(real Snowflake)       (simulated)      (simulated)       (Python print)
\```

## Setup requirements
1. Astronomer CLI installed
2. Docker Desktop running with WSL2 integration
3. Snowflake connection configured in Airflow UI (Admin → Connections)

## Connection details required
- Connection Id: snowflake_default
- Connection Type: Snowflake
- Account: your_account.region.azure
- Login: your_username
- Database: dbt_tutorial
- Schema: jaffle_shop
- Warehouse: dbt_tutorial_wh

## Airflow 3.x notes
This DAG is written for Airflow 3.x. Key differences from 2.x:
- schedule= not schedule_interval=
- SQLExecuteQueryOperator for Snowflake (not SnowflakeOperator)
- provide_context=True removed from PythonOperator
- airflow.providers.standard.operators.python (not airflow.operators.python)

## How to run
\```bash
cd ~/airflow-dbt-project
astro dev start
# Go to http://airflow-dbt-project.localhost:6563
# Trigger daily_data_pipeline manually
\```
