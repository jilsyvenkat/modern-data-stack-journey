-- BigQuery ML Reference — Day 12
-- These SQL patterns run in Google BigQuery
-- Similar concepts to Snowflake Cortex ML functions

-- ── Create a classification model ──────────────────────────
CREATE OR REPLACE MODEL `dbt_tutorial.customer_churn_model`
OPTIONS(
    model_type = 'logistic_reg',
    input_label_cols = ['is_churned'],
    max_iterations = 50
) AS
SELECT
    total_orders,
    avg_order_value,
    return_rate,
    days_since_last_order,
    days_since_signup,
    is_churned
FROM `dbt_tutorial.customer_features`;

-- ── Evaluate the model ──────────────────────────────────────
SELECT *
FROM ML.EVALUATE(
    MODEL `dbt_tutorial.customer_churn_model`
);

-- ── Make predictions ────────────────────────────────────────
SELECT
    customer_id,
    predicted_is_churned,
    predicted_is_churned_probs
FROM ML.PREDICT(
    MODEL `dbt_tutorial.customer_churn_model`,
    TABLE `dbt_tutorial.customer_features`
);

-- ── Explain predictions ─────────────────────────────────────
SELECT *
FROM ML.EXPLAIN_PREDICT(
    MODEL `dbt_tutorial.customer_churn_model`,
    TABLE `dbt_tutorial.customer_features`,
    STRUCT(3 AS top_k_features)
);

-- ── Time series forecasting ─────────────────────────────────
CREATE OR REPLACE MODEL `dbt_tutorial.order_forecast`
OPTIONS(
    model_type = 'ARIMA_PLUS',
    time_series_timestamp_col = 'order_date',
    time_series_data_col = 'order_count',
    horizon = 7,
    auto_arima = TRUE
) AS
SELECT order_date, order_count
FROM `dbt_tutorial.daily_order_counts`;

-- get forecast
SELECT *
FROM ML.FORECAST(
    MODEL `dbt_tutorial.order_forecast`,
    STRUCT(7 AS horizon)
);
