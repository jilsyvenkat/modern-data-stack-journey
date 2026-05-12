import ollama
import json
from datetime import datetime

print("MCP-Style Tool Calling Pattern")
print("=" * 60)

# ── MCP tool definitions ──────────────────────────────────────
# This mirrors how real MCP servers expose tools
MCP_TOOLS = [
    {
        "name": "query_database",
        "description": "Run a SQL query against the data warehouse",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The SQL query to execute"
                },
                "database": {
                    "type": "string",
                    "description": "Database name",
                    "default": "dbt_tutorial"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_pipeline_health",
        "description": "Check health status of data pipelines",
        "input_schema": {
            "type": "object",
            "properties": {
                "pipeline_name": {
                    "type": "string",
                    "description": "Name of pipeline to check"
                }
            },
            "required": ["pipeline_name"]
        }
    },
    {
        "name": "run_data_quality_check",
        "description": "Run data quality checks on a table",
        "input_schema": {
            "type": "object",
            "properties": {
                "table_name": {
                    "type": "string",
                    "description": "Table to check"
                },
                "checks": {
                    "type": "array",
                    "description": "List of checks to run",
                    "items": {"type": "string"}
                }
            },
            "required": ["table_name"]
        }
    },
    {
        "name": "send_alert",
        "description": "Send an alert to the data team",
        "input_schema": {
            "type": "object",
            "properties": {
                "severity": {
                    "type": "string",
                    "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
                },
                "message": {
                    "type": "string",
                    "description": "Alert message"
                },
                "channel": {
                    "type": "string",
                    "description": "Slack channel or email",
                    "default": "#data-alerts"
                }
            },
            "required": ["severity", "message"]
        }
    }
]

# ── MCP tool executor ─────────────────────────────────────────
def execute_mcp_tool(tool_name: str, parameters: dict) -> dict:
    print(f"\n  [MCP] Executing tool: {tool_name}")
    print(f"  [MCP] Parameters: {json.dumps(parameters, indent=4)}")

    if tool_name == "query_database":
        return {
            "status": "success",
            "rows_returned": 3,
            "data": [
                {"customer_id": 1, "orders": 2, "spend": 249.98},
                {"customer_id": 2, "orders": 1, "spend": 0.00},
                {"customer_id": 3, "orders": 1, "spend": 149.99},
            ],
            "execution_time_ms": 145
        }

    elif tool_name == "get_pipeline_health":
        return {
            "status": "healthy",
            "pipeline": parameters.get("pipeline_name"),
            "last_success": "2026-05-12 02:00:00",
            "success_rate_7d": 100.0,
            "avg_duration_seconds": 127,
            "next_scheduled": "2026-05-13 02:00:00"
        }

    elif tool_name == "run_data_quality_check":
        return {
            "table": parameters.get("table_name"),
            "checks_run": 4,
            "passed": 4,
            "failed": 0,
            "issues": [],
            "quality_score": 98.5,
            "timestamp": datetime.now().isoformat()
        }

    elif tool_name == "send_alert":
        return {
            "status": "sent",
            "alert_id": "ALT-2026-001",
            "severity": parameters.get("severity"),
            "channel": parameters.get("channel", "#data-alerts"),
            "timestamp": datetime.now().isoformat()
        }

    return {"status": "error", "message": f"Unknown tool: {tool_name}"}

# ── MCP conversation with tool calling ───────────────────────
def mcp_conversation(user_request: str):
    print(f"\n{'='*60}")
    print(f"USER REQUEST: {user_request}")
    print(f"{'='*60}")

    tools_json = json.dumps(MCP_TOOLS, indent=2)

    prompt = f"""You are a data platform assistant with access to
these MCP tools:

{tools_json}

User request: {user_request}

Respond with a JSON array of tool calls to fulfill this request.
Format:
[
  {{
    "tool": "tool_name",
    "parameters": {{"key": "value"}},
    "reason": "why you are calling this tool"
  }}
]

Then after the JSON, write "SUMMARY:" followed by what you found.
Only output valid JSON array followed by SUMMARY."""

    response = ollama.chat(
        model='llama3.2',
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = response['message']['content']

    # parse and execute tool calls
    try:
        start = response_text.find('[')
        end = response_text.find(']') + 1
        if start >= 0 and end > start:
            tool_calls = json.loads(response_text[start:end])

            print(f"\nAgent decided to call {len(tool_calls)} tool(s):")
            results = []

            for call in tool_calls:
                tool_name = call.get('tool')
                parameters = call.get('parameters', {})
                reason = call.get('reason', '')

                print(f"\n  Tool: {tool_name}")
                print(f"  Reason: {reason}")

                result = execute_mcp_tool(tool_name, parameters)
                results.append({
                    "tool": tool_name,
                    "result": result
                })
                print(f"  Result: {json.dumps(result)[:100]}...")

            # get summary from agent
            summary_start = response_text.find('SUMMARY:')
            if summary_start >= 0:
                print(f"\n{'='*60}")
                print("AGENT SUMMARY:")
                print(f"{'='*60}")
                print(response_text[summary_start + 8:].strip())

    except (json.JSONDecodeError, ValueError) as e:
        print(f"Parse note: {e}")
        print(f"Agent response: {response_text[:300]}")

# ── Test MCP pattern with data engineering requests ──────────
mcp_conversation(
    "Check if our data pipelines are healthy and run quality checks on the customers table"
)

mcp_conversation(
    "I need a report on customer spending — query the database and summarise the results"
)

mcp_conversation(
    "Something looks wrong with our data — check pipeline health and if there are issues send a HIGH severity alert to the data team"
)
