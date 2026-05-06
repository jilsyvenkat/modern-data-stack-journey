"What is the difference between Time Travel and Fail-safe?" — 
Time Travel is user-controlled up to 90 days. 
Fail-safe is Snowflake-controlled for 7 days after that, only recoverable by Snowflake support.
"When would you use Zero-Copy Cloning over a traditional copy?" — 
Any time you need an instant dev, UAT, or sandbox environment. 
No storage cost until data diverges, takes seconds instead of hours.
"What are Dynamic Tables and when would you use them over Airflow?" — 
For warehouse-native transformations needing automatic freshness. 
Airflow is still better for cross-system orchestration involving multiple tools.

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

  SELECT
    id,
    status,
    SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
        status,
        ['positive outcome', 'negative outcome']
    ) as outcome_category
FROM dbt_tutorial.jaffle_shop.raw_orders;
--AI function CLASSIFY_TEXT is not available for trial accounts.

CREATE OR REPLACE TABLE customer_feedback AS
SELECT
    1 as feedback_id,
    'The product arrived on time and was exactly as described.
     Customer service was helpful when I had a question.
     Would definitely order again from this company.' as feedback_text
UNION ALL
SELECT
    2,
    'Very disappointed with the quality. The item broke after
     two days of normal use. Contacted support three times
     with no resolution. Would not recommend.' as feedback_text;
--Table created
SELECT
    feedback_id,
    SNOWFLAKE.CORTEX.SUMMARIZE(feedback_text) as summary,
    SNOWFLAKE.CORTEX.SENTIMENT(feedback_text) as sentiment_score
FROM customer_feedback;
--AI function SUMMARIZE is not available for trial accounts.
