-- models/marts/customers.sql
with customers as (
    select * from {{ ref('stg_customers') }}  -- refers to YOUR staging model
),
...
