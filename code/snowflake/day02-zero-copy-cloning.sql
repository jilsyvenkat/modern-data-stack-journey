CREATE TABLE raw_customers_backup
CLONE raw_customers;

SELECT * FROM raw_customers_backup;

UPDATE raw_customers_backup
SET first_name = 'TEST'
WHERE id = 1;

-- clone changed
SELECT * FROM raw_customers_backup;

-- original untouched
SELECT * FROM raw_customers;

CREATE SCHEMA jaffle_shop_dev
CLONE jaffle_shop;

CREATE DATABASE dbt_tutorial_uat
CLONE dbt_tutorial;
