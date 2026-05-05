# Day 2 — Snowflake advanced features

## What I learned today
Four advanced Snowflake features that go well beyond basic querying —
Time Travel for historical data recovery, Zero-Copy Cloning for instant
environment copies, Dynamic Tables for automated pipeline refresh, and
Snowflake Cortex for running AI/LLM functions directly inside SQL.
Coming from an Oracle and DataStage background, these features represent
a significant leap in what a warehouse can do natively.

## Key concepts

- **Time Travel** — query data as it existed at any past point, up to
  90 days. After that, Fail-safe provides 7 more days managed by
  Snowflake internally. Critical for GDPR audit trails.

- **Zero-Copy Cloning** — instantly clone a table, schema, or entire
  database without duplicating storage. Only differences are stored
  after the clone. Game changer for dev/test environments.

- **Dynamic Tables** — define a transformation SQL once, set a target
  lag (e.g. 1 minute), and Snowflake keeps the table fresh
  automatically. No Airflow, no cron jobs needed for warehouse-native
  transformations.

- **Snowflake Cortex** — LLM functions callable directly in SQL.
  COMPLETE, SUMMARIZE, SENTIMENT, CLASSIFY_TEXT, TRANSLATE,
  EXTRACT_ANSWER. No Python, no API keys, no external services.

## What I built today
- Created and restored a table using Time Travel (OFFSET => -60)
- Cloned raw_customers table, modified clone, verified original untouched
- Cloned entire jaffle_shop schema and dbt_tutorial database instantly
- Created a Dynamic Table with 1-minute lag over customer + orders data
- Ran Snowflake Cortex sentiment analysis on customer feedback data(Ran into issues due to trial account)
- Ran Cortex CLASSIFY_TEXT on order statuses(Ran into issues due to trial account)

Time Travel:
\```sql
SELECT * FROM time_travel_test AT (OFFSET => -60);
ALTER TABLE time_travel_test SET DATA_RETENTION_TIME_IN_DAYS = 1;
\```

Zero-Copy Cloning:
\```sql
CREATE TABLE raw_customers_backup CLONE raw_customers;
CREATE SCHEMA jaffle_shop_dev CLONE jaffle_shop;
CREATE DATABASE dbt_tutorial_uat CLONE dbt_tutorial;
\```

Dynamic Tables:
\```sql
CREATE OR REPLACE DYNAMIC TABLE customer_order_summary
    TARGET_LAG = '1 minute'
    WAREHOUSE = dbt_tutorial_wh
AS SELECT ...
\```

Cortex:
\```sql
SELECT SNOWFLAKE.CORTEX.SENTIMENT(feedback_text) FROM customer_feedback;
SELECT SNOWFLAKE.CORTEX.SUMMARIZE(feedback_text) FROM customer_feedback;
\```

## How this connects to my work experience
At Optum managing GDPR and HIPAA compliance, Time Travel directly
answers the regulator question: "what did this record look like on
this date?" — no separate audit log table needed, it is built into
the warehouse.

Zero-Copy Cloning replaces the painful process of copying production
data to dev/UAT environments. At TCS this took hours and significant
storage. In Snowflake it is instantaneous and free until data diverges.

Dynamic Tables reduce orchestration complexity for warehouse-native
transformations — replacing crontab and Airflow jobs I managed at TCS
for straightforward refresh scenarios.

Snowflake Cortex is the biggest new capability — running sentiment
analysis, summarisation, and classification directly in SQL means
data teams can deliver AI features without a separate ML platform.

## talking points
- "Time Travel gives us a built-in audit trail — critical for GDPR
  data subject access requests and HIPAA compliance"
- "We use Zero-Copy Cloning to spin up dev environments instantly —
  no storage cost, no pipeline needed"
- "Dynamic Tables replaced several of our scheduled Airflow DAGs for
  warehouse-native transformations"
- "Snowflake Cortex lets our analysts run sentiment analysis in SQL —
  no Python environment, no API key management"

## Resources
- Snowflake Time Travel docs: docs.snowflake.com/en/user-guide/data-time-travel
- Snowflake Cloning docs: docs.snowflake.com/en/user-guide/object-clone
- Dynamic Tables: docs.snowflake.com/en/user-guide/dynamic-tables-about
- Snowflake Cortex: docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions
- My SQL scripts: /code/snowflake/
## Errors I faced today
-- try SENTIMENT first
SELECT SNOWFLAKE.CORTEX.SENTIMENT('This product is absolutely amazing!');
--AI function SENTIMENT is not available for trial accounts.
-- try TRANSLATE
SELECT SNOWFLAKE.CORTEX.TRANSLATE('Hello, how are you?', 'en', 'fr');
--AI function TRANSLATE is not available for trial accounts.
/*| Cortex COMPLETE not available | Trial accounts in North Europe
  Azure region have restricted Cortex access | Documented the
  functions and architecture — full hands-on to be completed
  when on a paid account or US region trial |*/
