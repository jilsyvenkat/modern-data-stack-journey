# Day 13 — Agentic AI & MCP protocol

## What I learned today
AI agents extend LLMs with the ability to take actions —
calling tools, observing results, and reasoning across multiple
steps until a goal is achieved. Built a data engineering agent
with 5 tools (query Snowflake, run dbt tests, check pipeline
status, get quality metrics, generate SQL) and an MCP-style
tool calling pattern. MCP (Model Context Protocol) is Anthropic's
open standard for connecting LLMs to external tools — the
universal connector that makes agentic AI practical at scale.
Discovered firsthand why agent tool reliability is the hardest
problem in production agentic systems — the LLM does not
reliably follow tool parameter schemas and requires defensive
coding patterns throughout.

## Key concepts

- **AI agent** — an LLM that can take actions. Has four
  components: LLM brain, tools, memory, and an execution
  loop (think → act → observe → repeat until goal achieved).

- **Tool calling** — the mechanism by which an agent calls
  external functions. Agent outputs structured JSON describing
  which tool to call and with what parameters. The LLM decides
  which tool to use based on tool descriptions.

- **Agent loop** — think → act → observe → think → act until
  goal achieved or max steps reached. Each step informed by
  previous tool results. Critical to set max_steps to prevent
  infinite loops.

- **Tool schema** — JSON schema defining a tool's name,
  description, and parameters. Tells the LLM what the tool
  does and how to call it. Poor descriptions lead to wrong
  tool selection. Even good descriptions do not guarantee
  correct parameter names.

- **MCP (Model Context Protocol)** — open standard by Anthropic
  for connecting LLMs to tools and data sources. Like USB-C
  for AI — universal connector enabling any LLM to use any
  MCP-compatible tool without custom integrations.

- **MCP server** — exposes tools, resources, and prompts via
  the MCP protocol. Examples: Snowflake MCP server, GitHub
  MCP server, Google Drive MCP server, Slack MCP server.

- **Defensive tool coding** — using **kwargs and fallback
  parameter matching to handle the LLM's creative parameter
  naming. Critical for production agent reliability.

## What I built today

**data_agent.py** — data engineering agent with 5 tools:
- query_snowflake — execute SQL queries
- run_dbt_test — run data quality tests
- check_pipeline_status — verify pipeline health
- get_data_quality_metrics — quality scores per table
- generate_sql — SQL from natural language
- Agent successfully completed 3 goals after fixing
  defensive parameter handling
- Key fix: all tools use **kwargs with multiple fallback
  parameter names to handle LLM's unpredictable naming

**mcp_pattern.py** — MCP-style tool calling with 4 tools:
- query_database — warehouse SQL execution
- get_pipeline_health — pipeline monitoring
- run_data_quality_check — quality validation
- send_alert — Slack/email notifications
- 3 user requests handled with structured tool calling
  and agent summaries

## Agent vs plain LLM vs RAG

| Approach | Input | Process | Output |
|----------|-------|---------|--------|
| Plain LLM | Question | Single inference | Answer from training |
| RAG | Question | Retrieve + generate | Answer from documents |
| Agent | Goal | Multi-step tool use | Action + answer |

## Agent loop in action — goal 1

\```
Goal: Check if daily_data_pipeline ran successfully

Step 1: Agent thinks → calls check_pipeline_status
        Result: status=success, rows=15420, duration=127s

Step 2: Agent thinks → DONE
        Answer: Pipeline ran successfully, processed 15420 rows
\```

## Agent loop in action — goal 2

\```
Goal: Data quality score for customers table

Step 1: Agent thinks → calls get_data_quality_metrics
        Result: quality_score=98.5, nulls=0, duplicates=0

Step 2: Agent thinks → DONE
        Answer: Score 98.5, data fresh within 2.5 hours,
                no nulls or duplicates found
\```

## Agent loop in action — goal 3 (the hard one)

\```
Goal: Summary of order data — count and status breakdown

Step 1: calls query_snowflake with COUNT query
        Result: count=3

Step 2: calls generate_sql with wrong params {n:3, table:orders}
        ERROR: unexpected keyword argument 'n'
        Fix: made generate_sql accept **kwargs

Step 3: calls run_dbt_test with wrong params {model_id:orders}
        ERROR: unexpected keyword argument 'model_id'
        Fix: made ALL tools accept **kwargs with fallbacks

Step 4: after fixes — agent completes successfully
\```

## MCP architecture

\```
LLM Client (Claude / Llama)
        │ MCP Protocol
        ▼
MCP Server (Snowflake)     → query tables, run SQL
MCP Server (GitHub)        → read/write code
MCP Server (Google Drive)  → access documents
MCP Server (Slack)         → send messages
MCP Server (Airflow)       → trigger DAGs
MCP Server (Zapier)        → thousands of integrations
\```

## Real MCP servers available in 2026
- Snowflake MCP server
- GitHub MCP server
- Google Drive MCP server
- Slack MCP server
- Jira MCP server
- Salesforce MCP server
- PostgreSQL MCP server
- Zapier MCP server (thousands of app integrations)

## The defensive tool coding pattern

Wrong approach — brittle:
\```python
def run_dbt_test(model_name: str) -> dict:
    # fails if LLM passes model_id or model or name
    print(f"Testing {model_name}")
\```

Correct approach — defensive:
\```python
def run_dbt_test(**kwargs) -> dict:
    model_name = (
        kwargs.get('model_name') or
        kwargs.get('model') or
        kwargs.get('model_id') or
        kwargs.get('name') or
        str(kwargs)
    )
    print(f"Testing {model_name}")
\```

This pattern is essential for any production agent tool.
The LLM will always find creative ways to name parameters
differently from your schema.

## How this connects to my work experience
At Optum managing 14 analysts, an AI agent with access to
Snowflake, dbt, and Airflow tools could handle first-line
data quality investigation automatically — checking pipeline
status, running dbt tests, querying for anomalies, and
sending alerts to the team. This reduces the manual triage
work that currently takes significant analyst time.

The MCP pattern is directly relevant to the Zapier interest
explored earlier in this journey — Zapier's MCP server
exposes thousands of integrations that an AI agent can call.
A data platform agent could trigger Zapier workflows for
notifications, ticket creation, and cross-system automation.

The tool schema pattern in mcp_pattern.py mirrors how
Airflow operators work — a defined interface with name,
description, and parameters. The mental model is identical:
a standardised way to define and call discrete units of work.

The debugging experience with wrong parameter names is
directly relevant to production — I now understand why
enterprise agent frameworks like LangChain add extensive
validation layers around tool calling. The LLM is
non-deterministic and will not always follow your schema.

## Talking points
- "AI agents extend LLMs with tool use — instead of answering
  from training data, the agent calls real systems, observes
  results, and reasons across multiple steps to complete a goal"
- "MCP is the USB-C of AI — a universal standard that lets
  any LLM connect to any tool without custom integrations.
  I built an MCP-style pattern where the agent decides which
  tools to call based on the user's goal"
- "For a data platform, agent tools map directly to operational
  tasks — query Snowflake, run dbt tests, check Airflow
  pipeline status, send Slack alerts. An agent can handle
  first-line data quality triage automatically"
- "I discovered firsthand why agent tool reliability is hard —
  the LLM does not reliably follow parameter schemas and passes
  creative names like model_id instead of model_name. Production
  agents need defensive **kwargs handling in every tool function"
- "The key to reliable agents is tool description quality —
  clear, specific descriptions of what each tool does and
  exactly what parameters it expects. Vague descriptions
  lead to wrong tool selection and wrong parameter names"

## Errors I hit and how I fixed them

| Error | Cause | Fix |
|---|---|---|
| TypeError: generate_sql() got unexpected keyword argument 'n' | LLM passed n and table instead of requirement | Made generate_sql accept **kwargs with fallback parameter name matching |
| TypeError: run_dbt_test() got unexpected keyword argument 'model_id' | LLM used model_id instead of model_name | Made ALL tool functions accept **kwargs with multiple fallback names |
| Agent calling wrong tools for order summary | Tool descriptions not specific enough for the goal | Core challenge of agent reliability — LLM is non-deterministic in tool selection |
| JSON parse errors from agent response | LLM sometimes adds explanation text around JSON | Added start/end bracket detection to extract JSON from mixed response |

## The production reliability lesson
This is the most important insight from Day 13:

Building an agent that works once in a demo is easy.
Building an agent that works reliably in production is hard.

The three layers of production agent reliability:
1. Tool descriptions — clear, specific, unambiguous
2. Tool implementation — defensive **kwargs, input validation
3. Error handling — feed errors back to agent for retry

Enterprise agent frameworks like LangChain, LlamaIndex,
and Anthropic's tool use API add all three layers
automatically. Understanding WHY they are needed — from
real debugging experience — makes you a much stronger
candidate for senior AI platform roles.

## Resources
- MCP protocol: modelcontextprotocol.io
- Anthropic MCP: anthropic.com/news/model-context-protocol
- LangChain agents: python.langchain.com/docs/concepts/agents
- LangGraph: langchain-ai.github.io/langgraph
- My code: /code/agents/
