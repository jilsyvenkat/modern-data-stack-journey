import ollama
import json
from datetime import datetime

dbt_test_results = {
    "run_date": datetime.now().isoformat(),
    "project": "jaffle_shop",
    "database": "dbt_tutorial",
    "schema": "jaffle_shop",
    "total_tests": 11,
    "passed": 10,
    "failed": 1,
    "test_details": [
        {"test": "not_null_customers_customer_id",      "status": "PASS"},
        {"test": "unique_customers_customer_id",         "status": "PASS"},
        {"test": "not_null_customers_first_name",        "status": "PASS"},
        {"test": "not_null_customers_last_name",         "status": "PASS"},
        {"test": "not_null_customers_number_of_orders",  "status": "PASS"},
        {"test": "source_not_null_raw_customers_id",     "status": "PASS"},
        {"test": "source_unique_raw_customers_id",       "status": "PASS"},
        {"test": "source_not_null_raw_orders_id",        "status": "PASS"},
        {"test": "source_unique_raw_orders_id",          "status": "PASS"},
        {"test": "source_not_null_raw_orders_status",    "status": "PASS"},
        {"test": "source_accepted_values_orders_status", "status": "FAIL",
         "details": "Found 2 rows with status=pending not in accepted values"},
    ]
}

prompt = f"""
Analyse these dbt test results and write a report for business
stakeholders who are not technical.

DBT TEST RESULTS:
{json.dumps(dbt_test_results, indent=2)}

Write a report with these sections:
1. EXECUTIVE SUMMARY (2 sentences)
2. WHAT PASSED (brief)
3. WHAT FAILED (plain English — business impact)
4. RECOMMENDED ACTION
5. RISK LEVEL (Low/Medium/High and why)

Keep under 250 words. Write for a Head of Data audience.
"""

response = ollama.chat(
    model='llama3.2',
    messages=[
        {
            'role': 'system',
            'content': """You are a senior data quality analyst who
            translates technical pipeline results into clear business
            language. You are concise and always include a recommended
            action."""
        },
        {
            'role': 'user',
            'content': prompt
        }
    ]
)

print("=" * 60)
print("DATA QUALITY REPORT")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)
print(response['message']['content'])
print("=" * 60)
