USE DATABASE dbt_tutorial;
USE SCHEMA jaffle_shop;
USE WAREHOUSE dbt_tutorial_wh;

-- remind yourself what data you have
SELECT * FROM raw_orders;
SELECT * FROM raw_customers;
SELECT * FROM customers;

----block2
-- create orders table with full Iceberg-like features
CREATE OR REPLACE TABLE orders_iceberg_demo (
    order_id        INTEGER,
    customer_id     INTEGER,
    order_date      DATE,
    status          VARCHAR(50),
    amount          FLOAT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- load data from your existing raw_orders seed
INSERT INTO orders_iceberg_demo (order_id, customer_id, order_date, status, amount)
SELECT
    id              as order_id,
    user_id         as customer_id,
    order_date::DATE as order_date,
    status,
    CASE
        WHEN status = 'completed' THEN 99.99
        WHEN status = 'returned'  THEN 49.99
        ELSE 0
    END             as amount
FROM raw_orders;

-- verify
SELECT * FROM orders_iceberg_demo ORDER BY order_id;

---block3
-- insert a new order
INSERT INTO orders_iceberg_demo
    (order_id, customer_id, order_date, status, amount)
VALUES
    (4, 1, '2024-01-04'::DATE, 'completed', 149.99),
    (5, 2, '2024-01-05'::DATE, 'pending',    79.99);

-- verify
SELECT * FROM orders_iceberg_demo ORDER BY order_id;

-- update an order
UPDATE orders_iceberg_demo
SET status = 'returned'
WHERE order_id = 4;

-- verify the update
SELECT * FROM orders_iceberg_demo ORDER BY order_id;

-- delete an order
DELETE FROM orders_iceberg_demo
WHERE order_id = 5;

-- final state
SELECT * FROM orders_iceberg_demo ORDER BY order_id;

--block4
-- query data as it was 2 minutes ago (before updates)
SELECT * FROM orders_iceberg_demo
AT (OFFSET => -60)
ORDER BY order_id;

-- query at a specific timestamp
SELECT * FROM orders_iceberg_demo
AT (TIMESTAMP => DATEADD(minute, -1, CURRENT_TIMESTAMP()))
ORDER BY order_id;

-- compare before and after
SELECT 'current' as version, order_id, status, amount
FROM orders_iceberg_demo
UNION ALL
SELECT 'before_changes' as version, order_id, status, amount
FROM orders_iceberg_demo AT (OFFSET => -120)
ORDER BY order_id, version;

--block5
-- add a new column without rewriting any data
ALTER TABLE orders_iceberg_demo
ADD COLUMN delivery_region VARCHAR(50);

-- add another column
ALTER TABLE orders_iceberg_demo
ADD COLUMN is_priority BOOLEAN DEFAULT FALSE;

-- update with new data
UPDATE orders_iceberg_demo
SET delivery_region = 'IRELAND',
    is_priority = TRUE
WHERE customer_id = 1;

UPDATE orders_iceberg_demo
SET delivery_region = 'UK',
    is_priority = FALSE
WHERE customer_id = 2;

-- old and new data coexist perfectly
SELECT * FROM orders_iceberg_demo ORDER BY order_id;

--block6
-- clone the table instantly for a dev environment
-- you already know this from Day 2!
CREATE TABLE orders_iceberg_dev
CLONE orders_iceberg_demo;

-- make changes in dev without affecting production
UPDATE orders_iceberg_dev
SET status = 'TEST'
WHERE order_id = 1;

-- production untouched
SELECT 'production' as env, order_id, status FROM orders_iceberg_demo
UNION ALL
SELECT 'development' as env, order_id, status FROM orders_iceberg_dev
ORDER BY order_id, env;

--block7
-- check storage breakdown
SELECT
    table_name,
    ROUND(active_bytes / (1024*1024), 2)      as active_mb,
    ROUND(time_travel_bytes / (1024*1024), 2) as time_travel_mb,
    ROUND(failsafe_bytes / (1024*1024), 2)    as failsafe_mb,
    ROUND(retained_for_clone_bytes / (1024*1024), 2) as clone_mb
FROM information_schema.table_storage_metrics
WHERE table_schema = 'JAFFLE_SHOP'
ORDER BY active_bytes DESC;
