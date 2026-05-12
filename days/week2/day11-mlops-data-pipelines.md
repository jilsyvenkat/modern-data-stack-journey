# Day 11 — MLOps & data pipelines for ML

## What I learned today
MLOps applies DevOps principles to machine learning — automating
the full lifecycle from data preparation through model training,
deployment, and monitoring. As a data engineer, the most important
insight is that data engineers own the most critical parts of
the ML lifecycle — raw data pipelines and feature engineering.
Without clean, consistent, fresh features, even the best ML
model fails. Built a complete feature engineering pipeline
producing 11 features per customer with validation and a
simulated churn risk model.

## Key concepts

- **Feature engineering** — transforming raw data into inputs
  for ML models. Aggregations, ratios, time-based calculations.
  Example: customer_order_count_last_30_days, return_rate,
  days_since_last_order.

- **Feature store** — centralised repository for ML features.
  Ensures training and serving use identical features.
  Prevents training-serving skew — the most common ML failure.

- **Training-serving skew** — model trained on features computed
  one way, served with features computed differently. Causes
  unexplained model performance degradation in production.

- **Data drift** — input data distribution changes over time.
  Customer behaviour shifts, new products launch. Model
  performance degrades silently without drift monitoring.

- **Point-in-time correct features** — when training on historical
  data, only use features available at that point in time.
  Prevents data leakage and over-optimistic model evaluation.

- **Feature validation** — check features for nulls, range
  violations, business logic errors before serving to model.
  Same concept as dbt tests but for ML features.

## What I built today

**feature_pipeline.py** — complete ML feature pipeline:
- Extracted raw customer and order data
- Engineered 11 features per customer:
  total_orders, completed_orders, returned_orders,
  failed_orders, total_spend, avg_order_value,
  return_rate, days_since_last_order, days_since_signup,
  is_high_value, is_at_risk
- Validated all features — 0 issues found
- Saved to feature store JSON with versioning
- Applied simple churn risk model using features

**ml_pipeline_patterns.md** — reference for 3 patterns:
batch, real-time, and hybrid feature pipelines with
tool recommendations for each scenario.

## Churn risk predictions from our pipeline

\```
Customer 1: 3 orders, 0.0 return rate, 43 days since order → LOW
Customer 2: 2 orders, 0.5 return rate, 14 days since order → MEDIUM
Customer 3: 1 order,  0.0 return rate, 28 days since order → LOW
\```

## ML pipeline patterns

| Pattern | Freshness | Tools | Use case |
|---------|-----------|-------|---------|
| Batch | Daily/hourly | Airflow + dbt + Snowflake | Churn, recommendations |
| Real-time | Sub-second | Kafka + Flink + Redis | Fraud, pricing |
| Hybrid | Mixed | All of above | Most enterprise ML |

## How this connects to my work experience
At Optum managing healthcare data, ML features for patient
risk scoring are critical. The feature pipeline built today
mirrors exactly what a clinical ML team needs — patient
behaviour aggregations, time-based features, risk flags —
all validated before serving to the model.

The validation step maps directly to my dbt testing work
from Day 6 — same principle, different context. Data quality
gates before data reaches its consumer, whether that consumer
is a BI dashboard or an ML model.

Training-serving skew is a governance concern I can speak
to from a HIPAA perspective — inconsistent feature computation
between training and production means the model is making
decisions based on different data than it was validated on.
That is a compliance risk in healthcare ML.

## Talking points
- "Data engineers own the most critical parts of MLOps —
  raw data pipelines and feature engineering. Without clean,
  consistent, fresh features the ML model fails regardless
  of how good the algorithm is."
- "I built a feature store pattern that prevents training-serving
  skew — features computed once, stored centrally, served
  identically to both training jobs and production models."
- "Feature validation is the same concept as dbt testing
  applied to ML inputs — null checks, range validation,
  business logic verification before features reach the model."
- "For real-time fraud detection you need Kafka feeding an
  online feature store like Redis — millisecond freshness.
  For churn prediction, daily batch features from Snowflake
  via Airflow are sufficient."

## Errors I hit and how I fixed them

| Error | Cause | Fix |
|---|---|---|
| Add yours here | | |

## Resources
- MLflow: mlflow.org
- Feast feature store: feast.dev
- Vertex AI Feature Store: cloud.google.com/vertex-ai/docs/featurestore
- Tecton: tecton.ai
- My code: /code/mlops/
