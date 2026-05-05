CREATE OR REPLACE DYNAMIC TABLE customer_order_summary
    TARGET_LAG = '1 minute'
    WAREHOUSE = dbt_tutorial_wh
AS
SELECT
    c.id as customer_id,
    c.first_name,
    c.last_name,
    COUNT(o.id) as total_orders,
    MIN(o.order_date) as first_order_date,
    MAX(o.order_date) as latest_order_date
FROM dbt_tutorial.jaffle_shop.raw_customers c
LEFT JOIN dbt_tutorial.jaffle_shop.raw_orders o ON c.id = o.user_id
GROUP BY 1, 2, 3;
--Dynamic table CUSTOMER_ORDER_SUMMARY successfully created. FULL refresh mode was selected because: This dynamic table contains a complex query. Refresh mode has been set to FULL. If you wish to override this automatic choice, please re-create the dynamic table and specify REFRESH_MODE=INCREMENTAL. For best results, we recommend reading https://docs.snowflake.com/user-guide/dynamic-table-performance-guide before setting the refresh mode to INCREMENTAL.



SELECT * FROM customer_order_summary;

SHOW DYNAMIC TABLES;

ALTER DYNAMIC TABLE customer_order_summary REFRESH;

SELECT * FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
    NAME => 'CUSTOMER_ORDER_SUMMARY'
));
