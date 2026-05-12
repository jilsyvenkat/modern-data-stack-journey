# ML Pipeline Patterns — Data Engineer Reference

## Pattern 1 — Batch feature pipeline
\```
Snowflake raw tables
        │ (daily Airflow DAG)
        ▼
dbt transformations
        │
        ▼
Feature engineering (Python)
        │
        ▼
Feature store (Snowflake table or Feast)
        │
        ▼
Model training job (weekly)
        │
        ▼
Model registry (MLflow)
\```
Best for: churn prediction, recommendation engines,
credit scoring — anywhere daily freshness is acceptable

## Pattern 2 — Real-time feature pipeline
\```
Source system events
        │ (Kafka topic)
        ▼
Stream processor (Flink/Kafka Streams)
        │ (sub-second)
        ▼
Online feature store (Redis)
        │
        ▼
Model serving API (FastAPI)
        │ (milliseconds)
        ▼
Real-time prediction
\```
Best for: fraud detection, real-time pricing,
personalisation — requires millisecond freshness

## Pattern 3 — Hybrid pipeline (most common in enterprise)
\```
Batch features (Snowflake → dbt → feature store)
        +
Streaming features (Kafka → Redis)
        │
        ▼
Feature retrieval layer
(combines batch + streaming features)
        │
        ▼
Model prediction
\```
Best for: most production ML systems combine both
batch historical features + real-time event features

## Key MLOps tools to know

| Tool | Purpose | Used by |
|------|---------|---------|
| MLflow | Experiment tracking, model registry | Most ML teams |
| Feast | Open source feature store | Google, Twitter |
| Tecton | Managed feature store | Enterprise |
| Vertex AI | Google ML platform | GCP shops |
| SageMaker | AWS ML platform | AWS shops |
| Azure ML | Microsoft ML platform | Azure shops |
| Airflow | Batch pipeline orchestration | Everyone |
| Kafka | Real-time feature pipelines | Real-time teams |
| dbt | Feature transformation layer | Modern data teams |

## Data engineer responsibilities in MLOps

1. Build and maintain feature pipelines
2. Ensure feature consistency between training and serving
3. Monitor feature drift and data quality
4. Manage feature store versioning
5. Build retraining triggers when data drifts
6. Optimise feature computation costs
7. Document features for ML team consumption
