# Day 12 — Snowflake Cortex & BigQuery ML

## What I learned today
Snowflake Cortex brings LLM and ML functions directly into SQL —
no Python, no external APIs, no data leaving Snowflake. Studied
the full Cortex function library and wrote SQL for all key
functions. Snowflake trial account in North Europe Azure region
restricted LLM function access, so pivoted to BigQuery ML where
all 7 blocks ran successfully — including a real ARIMA_PLUS time
series forecast producing 7 days of order predictions with 95%
confidence intervals. Combined Cortex architecture knowledge with
real BigQuery ML hands-on and local Ollama pipeline to demonstrate
the complete AI analytics story.

## Key concepts

- **Snowflake Cortex LLM functions** — COMPLETE, SUMMARIZE,
  SENTIMENT, CLASSIFY_TEXT, TRANSLATE, EXTRACT_ANSWER.
  Called directly in SQL. Data never leaves Snowflake.
  Requires paid account or supported region for full access.

- **Snowflake Cortex ML functions** — FORECAST, ANOMALY_DETECTION,
  CLASSIFICATION, REGRESSION, CONTRIBUTION_EXPLORER.
  ML models trained and served inside Snowflake without
  external ML platforms.

- **BigQuery ML** — same warehouse-native ML concept on GCP.
  CREATE MODEL, ML.EVALUATE, ML.PREDICT, ML.EXPLAIN_PREDICT,
  ML.FORECAST all in SQL. Directly relevant to GCP certification.

- **ARIMA_PLUS** — BigQuery ML's time series forecasting model.
  Automatically detects seasonality and trend. Returns
  forecast_value, standard_error, and confidence intervals.

- **Logistic regression in SQL** — CREATE MODEL with
  model_type=logistic_reg for binary classification.
  No Python, no scikit-learn, no data export needed.

- **AI analytics pipeline** — chain Cortex or BigQuery ML
  outputs with LLM generation for executive reporting.
  Raw data → ML insights → LLM summary → Board report.

## What I built today

**snowflake_cortex_demo.sql** — 8 SQL blocks written and
documented for Snowflake Cortex:
- customer_feedback_cortex table with 5 realistic reviews
- SENTIMENT analysis with positive/negative/neutral labels
- SUMMARIZE producing one-line summaries
- CLASSIFY_TEXT into 5 business categories
- COMPLETE for custom action recommendations
- customer_ai_insights VIEW joining all AI outputs
- ANOMALY_DETECTION on daily order counts
- Note: LLM functions unavailable on trial account —
  SQL documented and ready for paid environment

**bigquery_ml_reference.sql** — ran all 7 blocks successfully
in BigQuery console (console.cloud.google.com):
- Created customer_features table with 3 customers and
  churn labels for model training
- Created daily_order_counts table with 17 days of data
  including 2 injected anomalies (spike day 7, drop day 14)
- CREATE MODEL customer_churn_model (logistic regression)
  trained on total_orders, avg_order_value, return_rate,
  days_since_last_order, days_since_signup
- ML.EVALUATE — model evaluation metrics returned
- ML.PREDICT — churn predictions per customer
- CREATE MODEL order_forecast using ARIMA_PLUS time series
  with auto_arima=TRUE, horizon=7
- ML.FORECAST — 7-day order count forecast with 95%
  confidence intervals successfully returned

**Real BigQuery ML forecast output:**
\```
Date          Forecast   Std Error  Confidence  Lower   Upper
2024-01-18    50.09       1.81        0.95       46.55   53.64
2024-01-19    46.52       2.22        0.95       42.18   50.85
2024-01-20    48.67       2.56        0.95       43.16   53.18
2024-01-21    49.05       2.86        0.95       43.45   54.65
2024-01-22    47.47       3.14        0.95       41.33   53.60
2024-01-23    50.82       3.39        0.95       44.20   57.45
\```
Forecast matches historical average of ~50 orders/day.
Standard error increases over horizon — normal for forecasting.

**ai_analytics_pipeline.py** — end-to-end local pipeline:
- Simulated Cortex outputs using realistic feedback data
- Fed results to Ollama Llama 3.2 for board report generation
- Produced executive report with sentiment summary,
  anomaly alerts, and top 3 recommended actions
- Sentiment breakdown: 2 positive, 2 negative, 1 neutral

## Cortex function reference

| Function | Input | Output | Use case |
|----------|-------|--------|---------|
| SENTIMENT | text | -1 to 1 score | Customer feedback analysis |
| SUMMARIZE | long text | short summary | Report generation |
| CLASSIFY_TEXT | text + categories | category label | Issue routing |
| COMPLETE | model + prompt | generated text | Custom analysis |
| TRANSLATE | text + languages | translated text | Multi-language |
| ANOMALY_DETECTION | time series | anomaly flags | Pipeline monitoring |
| FORECAST | time series | future values | Demand forecasting |

## Snowflake Cortex vs BigQuery ML vs External API

| Factor | Snowflake Cortex | BigQuery ML | External API |
|--------|-----------------|-------------|--------------|
| Data location | Stays in Snowflake | Stays in BigQuery | Leaves boundary |
| Authentication | Snowflake creds | GCP creds | Separate API keys |
| SQL interface | Native | Native | Requires Python |
| HIPAA suitability | High | High | Requires BAA |
| Model choice | Limited | Limited | Many models |
| Cost model | Snowflake compute | BigQuery compute | Per token |
| Free tier | Restricted by region | Generous sandbox | Limited |

## How this connects to my work experience
At Optum the CLASSIFY_TEXT function maps directly to a real
need — patient feedback and support tickets arrive in free
text. Currently classified manually. Cortex CLASSIFY_TEXT
could automate routing into clinical concern, billing issue,
appointment scheduling, or general enquiry — all inside
Snowflake without PHI leaving the corporate boundary.

The ARIMA_PLUS forecast built in BigQuery ML today mirrors
what I would use for data pipeline monitoring — forecasting
expected record counts and alerting when actuals deviate
significantly from the forecast. This connects directly to
the DataOps work from Day 6.

For Optum's HIPAA environment, both Snowflake Cortex and
BigQuery ML keep data inside the platform boundary —
no Business Associate Agreement needed for external AI
vendors. This is a significant compliance advantage.

The GCP certification combined with real BigQuery ML hands-on
means I can architect AI solutions on either Snowflake or GCP
— important for multi-cloud environments.

## Talking Points
- "Snowflake Cortex runs LLM functions in SQL — SENTIMENT,
  SUMMARIZE, CLASSIFY_TEXT — without data leaving Snowflake.
  For HIPAA environments this is significant: AI on patient
  feedback without data leaving the account."
- "I built a real ARIMA_PLUS time series forecast in BigQuery
  ML producing 7-day order predictions with 95% confidence
  intervals — all in SQL, no Python, no data export."
- "Warehouse-native ML — whether Snowflake Cortex or BigQuery
  ML — eliminates the data movement risk that comes with
  exporting data to external ML platforms. Simpler architecture,
  better governance, lower cost."
- "When Snowflake Cortex LLM functions were unavailable on
  my trial account, I built an equivalent pipeline using
  Ollama locally — same architecture, self-hosted LLM,
  which is actually the preferred pattern for HIPAA
  environments."
- "The BigQuery ML and Snowflake Cortex ML patterns are
  architecturally identical — CREATE MODEL in SQL, evaluate,
  predict. My GCP certification plus Snowflake experience
  means I can work on either platform."

## Errors I hit and how I fixed them

| Error | Cause | Fix |
|---|---|---|
| AI function SENTIMENT not available | Trial account in North Europe Azure region restricts Cortex LLM functions | Documented all SQL patterns for paid environment. Pivoted to BigQuery ML for hands-on and ran ai_analytics_pipeline.py with Ollama locally |
| Cortex COMPLETE not available | Same trial account restriction | Same fix — all SQL written and ready, BigQuery ML used for real hands-on execution |

## Resources
- Snowflake Cortex docs: docs.snowflake.com/en/user-guide/snowflake-cortex
- Snowflake Cortex LLM functions: docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions
- BigQuery ML docs: cloud.google.com/bigquery/docs/bqml-introduction
- BigQuery ML forecasting: cloud.google.com/bigquery/docs/arima-single-time-series-forecasting-tutorial
- Google Cloud Console: console.cloud.google.com
- My SQL scripts: /code/cortex/
