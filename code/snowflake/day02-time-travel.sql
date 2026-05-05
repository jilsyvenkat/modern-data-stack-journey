USE DATABASE dbt_tutorial;
USE SCHEMA jaffle_shop;

CREATE OR REPLACE TABLE time_travel_test AS
SELECT * FROM raw_customers;

SELECT * FROM time_travel_test;

UPDATE time_travel_test
SET first_name = 'CHANGED'
WHERE id = 1;

SELECT * FROM time_travel_test;

-- go back 60 seconds
SELECT * FROM time_travel_test
AT (OFFSET => -60);


CREATE OR REPLACE TABLE time_travel_test AS
SELECT * FROM time_travel_test
AT (OFFSET => -60);

SELECT * FROM time_travel_test;

ALTER TABLE time_travel_test
SET DATA_RETENTION_TIME_IN_DAYS = 1;

SHOW TABLES LIKE 'time_travel_test';
