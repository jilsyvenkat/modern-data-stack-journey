import ollama
import json
from datetime import datetime

print("Data Engineering Agent")
print("=" * 60)

# ── Define tools the agent can use ───────────────────────────
# In production these would connect to real systems
# Here we simulate them to demonstrate the pattern

def query_snowflake(**kwargs) -> dict:
    """Execute a SQL query against Snowflake"""
    sql = (
        kwargs.get('sql') or
        kwargs.get('query') or
        kwargs.get('statement') or
        str(kwargs)
    )
    print(f"  [TOOL] query_snowflake: {str(sql)[:60]}...")
    if "COUNT" in str(sql).upper() and "orders" in str(sql).lower():
        return {"rows": [{"count": 3}], "status": "success"}
    elif "raw_customers" in str(sql).lower():
        return {
            "rows": [
                {"id": 1, "first_name": "Michael", "last_name": "P"},
                {"id": 2, "first_name": "Shawn",   "last_name": "M"},
                {"id": 3, "first_name": "Katharine","last_name": "R"},
            ],
            "status": "success"
        }
    elif "raw_orders" in str(sql).lower():
        return {
            "rows": [
                {"id": 1, "user_id": 1, "status": "completed", "amount": 99.99},
                {"id": 2, "user_id": 2, "status": "returned",  "amount": 49.99},
                {"id": 3, "user_id": 1, "status": "completed", "amount": 149.99},
            ],
            "status": "success"
        }
    elif "customers" in str(sql).lower():
        return {
            "rows": [
                {"customer_id": 1, "first_name": "Michael",
                 "number_of_orders": 2, "total_spend": 249.98},
                {"customer_id": 2, "first_name": "Shawn",
                 "number_of_orders": 1, "total_spend": 0},
                {"customer_id": 3, "first_name": "Katharine",
                 "number_of_orders": 1, "total_spend": 149.99},
            ],
            "status": "success"
        }
    return {"rows": [], "status": "success", "message": "No results"}

def run_dbt_test(**kwargs) -> dict:
    """Run dbt tests for a specific model"""
    model_name = (
        kwargs.get('model_name') or
        kwargs.get('model') or
        kwargs.get('model_id') or
        kwargs.get('name') or
        str(kwargs)
    )
    print(f"  [TOOL] run_dbt_test: {model_name}")
    return {
        "model": model_name,
        "tests_run": 4,
        "passed": 4,
        "failed": 0,
        "status": "all_passed"
    }

def check_pipeline_status(**kwargs) -> dict:
    """Check the status of a data pipeline"""
    pipeline_name = (
        kwargs.get('pipeline_name') or
        kwargs.get('pipeline') or
        kwargs.get('name') or
        kwargs.get('id') or
        str(kwargs)
    )
    print(f"  [TOOL] check_pipeline_status: {pipeline_name}")
    return {
        "pipeline": pipeline_name,
        "last_run": "2026-05-12 02:00:00",
        "status": "success",
        "duration_seconds": 127,
        "rows_processed": 15420
    }

def get_data_quality_metrics(**kwargs) -> dict:
    """Get data quality metrics for a table"""
    table_name = (
        kwargs.get('table_name') or
        kwargs.get('table') or
        kwargs.get('name') or
        kwargs.get('dataset') or
        str(kwargs)
    )
    print(f"  [TOOL] get_data_quality_metrics: {table_name}")
    return {
        "table": table_name,
        "total_rows": 3,
        "null_count": 0,
        "duplicate_count": 0,
        "freshness_hours": 2.5,
        "quality_score": 98.5
    }

def generate_sql(**kwargs) -> dict:
    """Generate SQL from a natural language requirement"""
    requirement = (
        kwargs.get('requirement') or
        kwargs.get('query') or
        kwargs.get('description') or
        kwargs.get('request') or
        kwargs.get('n') or
        str(kwargs)
    )
    print(f"  [TOOL] generate_sql: {str(requirement)[:50]}...")
    sql_map = {
        "top customers": """
            SELECT customer_id, first_name,
                   number_of_orders, total_spend
            FROM customers
            ORDER BY total_spend DESC LIMIT 5""",
        "order summary": """
            SELECT status, COUNT(*) as order_count,
                   SUM(amount) as total_amount
            FROM raw_orders
            GROUP BY status ORDER BY order_count DESC""",
        "orders": """
            SELECT status, COUNT(*) as order_count,
                   SUM(amount) as total_amount
            FROM raw_orders
            GROUP BY status ORDER BY order_count DESC""",
    }
    for key, sql in sql_map.items():
        if key.lower() in str(requirement).lower():
            return {"sql": sql, "status": "generated"}
    return {
        "sql": "SELECT * FROM customers LIMIT 10",
        "status": "generated",
        "note": "Generic query generated"
    }

TOOLS = {
    "query_snowflake": {
        "function": query_snowflake,
        "description": "Execute SQL query against Snowflake data warehouse",
        "parameters": {"sql": "The SQL query to execute"}
    },
    "run_dbt_test": {
        "function": run_dbt_test,
        "description": "Run dbt data quality tests for a model",
        "parameters": {"model_name": "Name of the dbt model to test"}
    },
    "check_pipeline_status": {
        "function": check_pipeline_status,
        "description": "Check if a data pipeline ran successfully",
        "parameters": {"pipeline_name": "Name of the pipeline to check"}
    },
    "get_data_quality_metrics": {
        "function": get_data_quality_metrics,
        "description": "Get data quality metrics for a table",
        "parameters": {"table_name": "Name of the table to check"}
    },
    "generate_sql": {
        "function": generate_sql,
        "description": "Generate SQL from natural language requirement",
        "parameters": {"requirement": "Natural language description of what you need"}
    },
}

# ── Agent executor ────────────────────────────────────────────
def run_agent(goal: str, max_steps: int = 5):
    print(f"\n{'='*60}")
    print(f"AGENT GOAL: {goal}")
    print(f"{'='*60}")

    # build tool descriptions for the prompt
    tools_desc = "\n".join([
        f"- {name}: {info['description']}"
        for name, info in TOOLS.items()
    ])

    conversation = []
    step = 0

    while step < max_steps:
        step += 1
        print(f"\nStep {step}:")

        # build prompt
        system_prompt = f"""You are a data engineering agent.
You have access to these tools:
{tools_desc}

To use a tool, respond with ONLY a JSON object in this exact format:
{{"tool": "tool_name", "parameters": {{"param_name": "param_value"}}}}

When you have enough information to answer the goal, respond with:
{{"tool": "DONE", "answer": "your final answer here"}}

Always use a tool first to gather information before answering.
Never make up data — always use tools to get real information."""

        # add goal to conversation
        if step == 1:
            conversation.append({
                "role": "user",
                "content": f"Goal: {goal}"
            })

        response = ollama.chat(
            model='llama3.2',
            messages=[
                {"role": "system", "content": system_prompt}
            ] + conversation
        )

        agent_response = response['message']['content'].strip()
        print(f"  Agent thinks: {agent_response[:100]}...")

        # parse agent response
        try:
            # extract JSON from response
            start = agent_response.find('{')
            end = agent_response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = agent_response[start:end]
                action = json.loads(json_str)
            else:
                print("  Could not parse JSON — ending")
                break

            # check if done
            if action.get('tool') == 'DONE':
                print(f"\n{'='*60}")
                print("AGENT FINAL ANSWER:")
                print(f"{'='*60}")
                print(action.get('answer', 'No answer provided'))
                return action.get('answer')

            # execute the tool
            tool_name = action.get('tool')
            parameters = action.get('parameters', {})

            if tool_name in TOOLS:
                tool_result = TOOLS[tool_name]['function'](**parameters)
                print(f"  Tool result: {str(tool_result)[:100]}...")

                # add to conversation
                conversation.append({
                    "role": "assistant",
                    "content": agent_response
                })
                conversation.append({
                    "role": "user",
                    "content": f"Tool result: {json.dumps(tool_result)}"
                })
            else:
                print(f"  Unknown tool: {tool_name}")
                break

        except json.JSONDecodeError:
            print(f"  JSON parse error — agent may be done")
            print(f"\nAgent response: {agent_response}")
            return agent_response

    print("\nMax steps reached")
    return None

# ── Run agent with different goals ───────────────────────────
run_agent("Check if the daily_data_pipeline ran successfully and tell me how many rows were processed")

run_agent("What is the data quality score for the customers table and are there any issues?")

run_agent("Give me a summary of our order data — how many orders do we have and what is the status breakdown?")
