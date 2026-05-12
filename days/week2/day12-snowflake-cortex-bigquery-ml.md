# Day 12 — Snowflake Cortex & BigQuery ML

## What I learned today
Snowflake Cortex brings LLM and ML functions directly into SQL —
no Python, no external APIs, no data leaving Snowflake. Built
a complete customer intelligence pipeline using SENTIMENT,
SUMMARIZE, CLASSIFY_TEXT, and COMPLETE functions on real feedback
data. Understood BigQuery ML patterns for GCP environments.
Combined Cortex outputs with Ollama to generate board-level
executive reports — the full AI analytics pipeline from raw
feedback to actionable board insights.

## Key concepts

- **Snowflake Cortex LLM functions** — COMPLETE, SUMMARIZE,
  SENTIMENT, CLASSIFY_TEXT, TRANSLATE, EXTRACT_ANSWER.
  Called directly in SQL. Data never leaves Snowflake.

- **Snowflake Cortex ML functions** — FORECAST, ANOMALY_DETECTION,
  CLASSIFICATION, REGRESSION. ML models trained and served
  inside Snowflake without external ML platforms.

- **BigQuery ML** — same concept on GCP. CREATE MODEL, ML.EVALUATE,
  ML.PREDICT, ML.EXPLAIN_PREDICT all in SQL. Directly relevant
  to GCP certification.

- **AI analytics pipeline** — chain multiple AI capabilities:
  Cortex SENTIMENT scores → CLASSIFY_TEXT categories →
  COMPLETE for recommendations → LLM for executive summary.

- **Customer intelligence view** — CREATE VIEW combining
  customer data with AI-generated insights. Analysts query
  the view with SQL and get sentiment, summary, and category
  alongside raw data.

## What I built today

**snowflake_cortex_demo.sql** — 8 SQL blocks:
- Customer feedback table with 5 realistic reviews
- SENTIMENT analysis with positive/negative/neutral labels
- SUMMARIZE producing one-line summaries
- CLASSIFY_TEXT into 5 business categories
- COMPLETE for custom action recommendations
- customer_ai_insights VIEW joining all AI outputs
- ANOMALY_DETECTION on daily order counts

**bigquery_ml_reference.sql** — BigQuery ML patterns:
- CREATE MODEL for classification and time series
- ML.EVALUATE, ML.PREDICT, ML.EXPLAIN_PREDICT
- ARIMA_PLUS for order volume forecasting

**ai_analytics_pipeline.py** — end-to-end pipeline:
- Cortex outputs fed to Ollama
- Board-level executive report generated
- Sentiment breakdown and anomaly count

## Cortex function reference

| Function | Input | Output | Use case |
|----------|-------|--------|---------|
| SENTIMENT | text | -1 to 1 score | Customer feedback analysis |
| SUMMARIZE | long text | short summary | Report generation |
| CLASSIFY_TEXT | text + categories | category label | Issue routing |
| COMPLETE | model + prompt | generated text | Custom analysis |
| TRANSLATE | text + languages | translated text | Multi-language support |
| ANOMALY_DETECTION | time series | anomaly flags | Pipeline monitoring |
| FORECAST | time series | future values | Demand forecasting |

## Snowflake Cortex vs external LLM APIs

| Factor | Snowflake Cortex | External API |
|--------|-----------------|--------------|
| Data location | Stays in Snowflake | Leaves your boundary |
| Authentication | Snowflake credentials | Separate API keys |
| Cost model | Snowflake compute | Per token billing |
| SQL integration | Native | Requires Python |
| HIPAA suitability | High | Requires BAA |
| Model choice | Limited selection | Many models |

## How this connects to my work experience
At Optum, the CLASSIFY_TEXT function maps directly to a real
need — patient feedback and support tickets arrive in free
text. Currently classified manually. Cortex CLASSIFY_TEXT
could automate routing into: clinical concern, billing issue,
appointment scheduling, general enquiry — all inside Snowflake
without PHI leaving the corporate boundary.

The ANOMALY_DETECTION function on daily order counts mirrors
exactly what I would use on data pipeline metrics — detecting
when record counts spike or drop unexpectedly, triggering
Airflow alerts automatically.

The BigQuery ML patterns are directly relevant to GCP
certification — being able to speak to CREATE MODEL and
ML.PREDICT in SQL demonstrates the same AI capability
on GCP that Cortex provides on Snowflake.

## Talking points
- "Snowflake Cortex runs LLM functions in SQL — SENTIMENT,
  SUMMARIZE, CLASSIFY_TEXT — without data leaving Snowflake.
  For HIPAA environments this is significant: AI on patient
  feedback without a BAA or data leaving the account."
- "I built a customer intelligence view combining raw feedback
  with AI-generated sentiment scores, summaries, and issue
  categories. Analysts query it with standard SQL — no Python,
  no ML knowledge needed."
- "Cortex ANOMALY_DETECTION on pipeline metrics is a DataOps
  pattern — automatically flag when record counts deviate
  from normal, triggering Airflow alerts before business
  impact is felt."
- "BigQuery ML and Snowflake Cortex ML solve the same problem
  differently — ML in SQL inside your warehouse. The GCP
  certification combined with Snowflake hands-on means I
  can architect AI solutions on either platform."

## Errors I hit and how I fixed them

| Error | Cause | Fix |
|---|---|---|
| Cortex LLM functions unavailable | Trial account in North Europe Azure region has restricted Cortex access | Ran ai_analytics_pipeline.py locally with Ollama simulating Cortex outputs. Full Cortex access available on paid accounts or US region. |


## Resources
- Snowflake Cortex docs: docs.snowflake.com/en/user-guide/snowflake-cortex
- BigQuery ML docs: cloud.google.com/bigquery/docs/bqml-introduction
- Cortex LLM functions: docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions
- My SQL scripts: /code/cortex/
