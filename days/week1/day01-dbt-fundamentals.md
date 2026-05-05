# Day 1 — dbt fundamentals

## What I learned today
dbt (data build tool) is a transformation framework that lets you write
data transformations as plain SQL SELECT statements, with built-in
dependency management, testing, and documentation. Coming from 20 years
of Informatica and DataStage, this is the modern code-first replacement
for the T in ETL — running transformations inside the warehouse rather
than outside it.

## Key concepts

- **dbt seed** — loads CSV files as tables into Snowflake.
  Real-world use: version-controlled lookup tables (country codes,
  cost centres, GDPR data category mappings)

- **ref()** — creates dependencies between dbt models, builds the
  lineage DAG automatically. Snowflake runs models in the correct
  order based on these references.

- **source()** — points to raw tables loaded by upstream pipelines,
  declared in sources.yml for lineage tracking.

- **Lineage graph** — auto-generated visual DAG showing how every
  model depends on every other. Always up to date because it's
  generated from actual code, not written manually.

## What I built today
- Installed dbt-snowflake inside a Python virtual environment on WSL2
- Connected dbt Core to a Snowflake free trial (North Europe / Azure)
- Created seed files: raw_customers.csv and raw_orders.csv
- Built customers.sql mart model using ref() and source()
- Successfully ran dbt seed, dbt run, dbt docs generate
- Opened lineage graph at localhost:8080 in browser

## Errors I hit and how I fixed them

| Error | Cause | Fix |
|---|---|---|
| externally-managed-environment | Ubuntu 24 protects system Python | Created venv with python3 -m venv ~/.dbt-env |
| python3-venv not found | Package not installed by default | sudo apt install python3.12-venv |
| 404 Not Found on Snowflake | Account identifier had httpts:// prefix | Removed URL prefix, used bare account ID |
| Project path not found | Running dbt debug from wrong folder | cd into jaffle_shop project folder first |
| invalid identifier CUSTOMER_ID | raw_orders uses user_id not customer_id | Aliased user_id as customer_id in CTE |
| Two models named customers | Created customers.sql in two locations | Deleted duplicate from root models/ folder |

## Commands used today

\```bash
# environment setup
sudo apt install python3.12-venv
python3 -m venv ~/.dbt-env
source ~/.dbt-env/bin/activate
pip install dbt-snowflake

# project setup
dbt init jaffle_shop
dbt debug

# running dbt
dbt seed
dbt run
dbt docs generate
dbt docs serve
\```

## Folder structure created

\```
jaffle_shop/
├── dbt_project.yml
├── seeds/
│   ├── raw_customers.csv
│   └── raw_orders.csv
└── models/
    └── marts/
        └── customers.sql
\```

## How this connects to my work experience
At TCS I used Informatica and DataStage for ETL pipelines. dbt replaces
the transformation layer with plain SQL that lives in Git — giving
lineage, testing, and documentation for free. The ref() dependency
concept is similar to job sequencing in DataStage but visual,
version-controlled, and auto-documented.

At Optum, dbt would replace manual SQL scripts run via cron jobs —
every transformation would be traceable, testable, and visible in
the lineage graph. Significant improvement for GDPR data lineage
requirements.

- "I moved from legacy ETL thinking to ELT — dbt handles transformations
  inside Snowflake using SQL I already know, with lineage and testing built in"
- "dbt gave us lineage, testing, and documentation from a single codebase
  committed to Git — no separate documentation effort needed"
- "Every transformation is a SELECT statement — reviewable in a pull request
  like any other code change"

## Resources
- dbt Learn: https://courses.getdbt.com
- dbt docs: https://docs.getdbt.com
- My working code: /code/dbt/
