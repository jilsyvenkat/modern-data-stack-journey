# Day 4 — Apache Airflow & modern orchestration

## What I learned today
Apache Airflow is a workflow orchestration platform that schedules,
monitors, and manages the order of execution of tasks across an entire
data pipeline. Coming from crontab and DataStage job sequences at TCS
and Optum, Airflow replaces informal dependency management with a
visual, code-driven, fully observable pipeline. Every task is tracked,
every failure can be retried automatically, every run is logged, and
the entire pipeline is defined in Python code that lives in Git.
Installed Airflow locally via Astronomer CLI on Docker, built a
4-task DAG, and watched it execute successfully in the Airflow UI.

## Key concepts

- **DAG (Directed Acyclic Graph)** — the core unit of Airflow. A
  Python file defining tasks and their dependencies. Lives in the
  dags/ folder. Versioned in Git like any other code. Acyclic means
  tasks flow in one direction only — no loops.

- **Task** — a single unit of work inside a DAG. Can be a Python
  function, a shell command, a SQL query, a dbt run, an API call.
  Each task is independent, trackable, and retryable.

- **Operator** — the template for a task. Airflow has hundreds of
  built-in operators:
  - PythonOperator — runs a Python function
  - BashOperator — runs a shell command
  - SnowflakeOperator — runs SQL on Snowflake
  - dbt operators via Astronomer Cosmos

- **>> operator** — defines task dependency in Python code.
  task1 >> task2 means task2 only starts after task1 succeeds.
  This is how Airflow builds the DAG structure from code.

- **Schedule** — cron expression defining when the DAG runs.
  '0 2 * * *' means every day at 2am. Can also be triggered manually.

- **Trigger Rule** — controls when a task runs relative to upstream
  tasks. Default is all_success — task only runs if all upstream
  tasks succeeded.

- **Retry** — retries=2, retry_delay=timedelta(minutes=5) means
  Airflow automatically retries a failed task twice with a 5 minute
  gap before marking it as failed.

## What I built today
- Installed Astronomer CLI on WSL2
- Started Airflow locally via Docker (astro dev start)
- Accessed Airflow UI at http://airflow-dbt-project.localhost:6563
- Created daily_pipeline.py with 4 tasks:
  1. check_snowflake_data — PythonOperator simulating Snowflake check
  2. run_dbt_models — BashOperator simulating dbt run
  3. test_dbt_models — BashOperator simulating dbt test
  4. notify_completion — PythonOperator sending completion message
- Triggered DAG manually and watched all 4 tasks succeed
- Verified task logs showing correct output from each operator
- Viewed the visual DAG graph showing task dependency flow
- Total pipeline duration: 7.838 seconds end to end

## DAG graph structure

\```
check_snowflake_data → run_dbt_models → test_dbt_models → notify_completion
PythonOperator         BashOperator     BashOperator       PythonOperator
     3.160s               0.150s           0.145s             0.160s
\```

## Task Instances output (from Airflow UI)

\```
Task                  State    Operator         Duration
────────────────────────────────────────────────────────
check_snowflake_data  Success  PythonOperator   00:00:03.160
run_dbt_models        Success  BashOperator     00:00:00.150
test_dbt_models       Success  BashOperator     00:00:00.145
notify_completion     Success  PythonOperator   00:00:00.160
────────────────────────────────────────────────────────
Total DAG duration:                             00:00:07.838
\```

## Errors I hit and how I fixed them

| Error | Cause | Fix |
|---|---|---|
| Ports not available: 5432 | Windows blocking PostgreSQL port | Used astro dev start --postgres-port 5433 |
| DAG Import Error: unexpected keyword argument 'schedule_interval' | Airflow 3.x renamed schedule_interval to schedule | Changed schedule_interval= to schedule= |
| DAG not appearing after 5 minutes | Database migration needed | Ran airflow db migrate inside astro dev bash |
| cannot import name 'SnowflakeOperator' | Class renamed in newer Snowflake provider | Changed to SnowflakeSqlApiOperator as SnowflakeOperator |
| Invalid arguments: provide_context=True | Removed in Airflow 3.x — context auto injected | Removed provide_context=True from PythonOperator |
| airflow.operators.python deprecated | Moved to providers package in Airflow 3.x | Use airflow.providers.standard.operators.python |
| AttributeError: NoneType has no attribute public_key | SnowflakeSqlApiOperator requires JWT key pair not password | Switched to SQLExecuteQueryOperator which uses username/password |
| Connection test disabled | Astronomer disables it by default | Added AIRFLOW__CORE__TEST_CONNECTION=Enabled to .env file |

## Key Airflow 3.x breaking change
Airflow 3.0 renamed `schedule_interval` to `schedule` — a breaking
change from Airflow 2.x. This catches out many experienced Airflow
users upgrading from 2.x. Always check the Airflow version when
reading documentation or Stack Overflow answers.

## The DAG Python code

\```python
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
    description='Extract from Snowflake, transform with dbt, notify',
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
        bash_command='echo "Running dbt models... dbt run completed"',
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
\```

## Orchestration tool comparison

| Tool | Best for | Tradeoff |
|------|----------|----------|
| Airflow | Enterprise, large ecosystem, battle-tested | Complex to operate, verbose syntax |
| Prefect | Modern teams, clean Python syntax, fast setup | Smaller ecosystem, less enterprise adoption |
| Dagster | dbt-first teams, asset-oriented thinking | Steeper learning curve, newer |

## Astronomer vs self-managed Airflow

Astronomer is the managed Airflow platform — it handles Docker setup,
upgrades, and local development via the Astro CLI. In production,
Astronomer Cloud runs Airflow on Kubernetes without you managing the
infrastructure. Self-managed Airflow gives more control but requires
significant DevOps effort. For most enterprise teams Astronomer is
the right choice.

## How this connects to my work experience
At TCS I used crontab for scheduling and DataStage job sequences
for dependencies — both brittle, both invisible, both requiring
manual intervention on failure.

At Optum, managing 14 analysts and IRE & UK data pipelines, Airflow
would replace ad-hoc scheduling with observable, retryable,
dependency-aware pipelines. Every pipeline change reviewed in a
pull request. Every failure alerted automatically. Every run logged
for audit — directly supporting GDPR compliance requirements.

The >> operator replaces the informal "run this after that"
assumptions with explicit, version-controlled dependencies that
are visible to the whole team in one UI.

## Airflow 3.x breaking changes — learned the hard way

This was the most valuable part of Day 4. Running on Astronomer with
Airflow 3.x exposed four breaking changes from Airflow 2.x that trip
up experienced users:

| Airflow 2.x | Airflow 3.x | Impact |
|-------------|-------------|--------|
| schedule_interval= | schedule= | DAG import error |
| SnowflakeOperator | SnowflakeSqlApiOperator | Import error |
| provide_context=True | Removed — auto injected | TypeError on PythonOperator |
| airflow.operators.python | airflow.providers.standard.operators.python | Deprecation warning |
| SnowflakeSqlApiOperator (JWT) | SQLExecuteQueryOperator | JWT key pair needed for SQL API |

Key lesson: always check which Airflow version is running before
copying code from documentation or Stack Overflow. Most online
examples are still written for Airflow 2.x.

## Real Snowflake connection — what worked

After trying SnowflakeOperator and SnowflakeSqlApiOperator, the
correct operator for username/password authentication in Airflow 3
is SQLExecuteQueryOperator from airflow.providers.common.sql:

\```python
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

task_check_data = SQLExecuteQueryOperator(
    task_id='check_snowflake_data',
    conn_id='snowflake_default',
    sql="SELECT COUNT(*) FROM dbt_tutorial.jaffle_shop.raw_orders;",
)
\```

Connection was configured in Airflow UI under Admin → Connections:
- Connection Type: Snowflake
- Account: ll07743.north-europe.azure
- Login: JILSY711
- Database: dbt_tutorial
- Schema: jaffle_shop
- Warehouse: dbt_tutorial_wh

## Talking points
- "Airflow DAGs are Python code in Git — every pipeline change is
  reviewed in a pull request, not clicked through a GUI. This gives
  us full auditability of pipeline changes."
- "The >> operator makes dependencies explicit — task2 cannot run
  unless task1 succeeds, with automatic retry on failure. No more
  2am phone calls about a job that ran before its dependency."
- "We use retries=2 with retry_delay=5min — transient failures like
  network timeouts are handled automatically without waking anyone up."
- "For our dbt-Snowflake stack I would evaluate Dagster for its
  native asset awareness, but Airflow with Astronomer Cosmos gives
  similar capability with a larger operator ecosystem."
- "Airflow 3.x introduced breaking changes from 2.x — schedule_interval
  is now schedule, and the UI has been significantly redesigned.
  Always pin your Airflow version in production."

## Resources
- Astronomer docs: docs.astronomer.io
- Airflow docs: airflow.apache.org/docs
- Airflow 3.0 migration guide: airflow.apache.org/docs/apache-airflow/stable/migration-guide
- My DAG code: /code/airflow/daily_pipeline.py
