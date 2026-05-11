# Day 8 — LLM APIs & prompt engineering

## What I learned today
LLMs are neural networks trained on vast text that can understand
and generate language, code, and analytical reasoning. As a data
engineering leader, the key capability is not building models —
it is integrating LLM APIs into data products and pipelines.
Built three Python scripts today: a basic API call using Ollama
running locally, a real-world dbt report summariser that converts
technical test results into business language, and a prompt
engineering demonstration showing five techniques that dramatically
change output quality. Started with Google Gemini API but switched
to Ollama due to free tier quota exhaustion — which turned out to
be the better learning outcome as self-hosted LLMs are increasingly
relevant for HIPAA and GDPR environments.

## Key concepts

- **LLM API** — a REST endpoint that accepts text input and returns
  generated text. Always has: model, system prompt, user message,
  max_tokens. Ollama provides the same interface locally.

- **System prompt** — instructions that define how the model behaves
  for the entire conversation. Sets persona, tone, constraints,
  and output format. The single biggest lever for output quality.

- **Tokens** — the unit of LLM billing and context limits. Roughly
  4 characters = 1 token. 1000 tokens ≈ 750 words. Always monitor
  token usage in production cloud APIs.

- **Temperature** — controls randomness. 0 = deterministic/factual.
  1 = creative/varied. For data pipelines always use 0. For creative
  tasks use 0.7 to 1.0.

- **Context window** — maximum tokens the model can process at once.
  Claude supports up to 200k tokens — can process entire codebases.
  Llama 3.2 supports 128k tokens locally.

- **Self-hosted LLM** — an LLM running on your own hardware with no
  external API calls. Critical for HIPAA/GDPR environments where
  data cannot leave the corporate boundary.

## Prompt engineering techniques

| Technique | When to use | Example |
|-----------|------------|---------|
| Zero-shot | Simple, clear tasks | "Summarise this text" |
| Role prompting | Domain-specific analysis | "You are a Snowflake DBA..." |
| Chain of thought | Complex reasoning | "Think step by step..." |
| Few-shot | Consistent classification | Show 2-3 examples first |
| Output formatting | Feeding results to code | "Respond only with JSON" |

## What I built today

- **first_api_call.py** — Ollama/Llama 3.2 API call with system
  prompt running completely locally. No API key, no cost, no quota
  limits. Asked about Apache Iceberg from a Head of Data perspective.

- **dbt_report_summariser.py** — converts dbt test results JSON
  into a structured business report with Executive Summary, Risk
  Level, and Recommended Action. Directly relevant to Optum work
  where technical results need to be communicated to non-technical
  stakeholders.

- **prompt_engineering.py** — same SQL query asked five different
  ways demonstrating how dramatically prompting technique affects
  output quality. Role prompting and chain of thought produced
  the most actionable, Snowflake-specific advice.

## Ollama — self-hosted LLMs

Ollama runs LLMs completely locally — no API key, no cost,
no quota limits, no data leaving your machine.

Why this matters for enterprise data engineering:
- HIPAA/GDPR compliance — sensitive patient or customer data
  never sent to external APIs
- No per-token costs at scale — process millions of records
  without API bills
- Air-gapped environments — works in secure enterprise networks
  that block external API calls
- Consistent availability — no rate limits, no quota exhaustion

Commands used:
\```bash
sudo apt-get install zstd              # required dependency
curl -fsSL https://ollama.com/install.sh | sh  # install Ollama
ollama pull llama3.2                   # download model (~2GB)
ollama run llama3.2 "hello"            # test it
ollama list                            # see installed models
\```

Python integration:
\```python
import ollama

response = ollama.chat(
    model='llama3.2',
    messages=[
        {'role': 'system', 'content': 'You are a data expert'},
        {'role': 'user',   'content': 'Your question here'}
    ]
)
print(response['message']['content'])
\```

## Real-world data engineering use cases for LLMs

- **Data quality reporting** — convert technical dbt test failures
  to plain English reports for CDO/Head of Data audience
- **SQL optimisation** — paste a slow query, get optimisation advice
  with improved query shown
- **Documentation generation** — auto-generate dbt model descriptions
  from SQL code
- **Data contract validation** — check if incoming data matches
  expected schema and business rules
- **Anomaly explanation** — "explain why this metric dropped 40%"
- **Pipeline debugging** — paste error logs, get root cause analysis

## The dbt report summariser — why it matters

Raw dbt output that a CDO cannot interpret:
\```json
{
  "total_tests": 11,
  "passed": 10,
  "failed": 1,
  "test_details": [
    {"test": "source_accepted_values_orders_status",
     "status": "FAIL",
     "details": "Found 2 rows with status=pending"}
  ]
}
\```

What the LLM produced automatically:
\```
EXECUTIVE SUMMARY
Pipeline functioning correctly with majority of tests passing.
One test failed due to unexpected values in orders status column.

WHAT FAILED
Two rows have status=pending which is not an accepted value.
Potential issue with data validation in the pipeline.

RECOMMENDED ACTION
Review and refine data validation for the orders status column.

RISK LEVEL: Medium
Not critical but requires prompt attention.
\```

In production: replace hardcoded JSON with dbt's actual
target/run_results.json file — making the entire report
fully automated after every CI/CD pipeline run.

## Prompt engineering results — same SQL query, five approaches

Query tested: SELECT * FROM orders WHERE UPPER(status) = 'COMPLETED'

| Technique | Output quality | Key insight |
|-----------|---------------|-------------|
| Zero-shot | Basic — mentioned UPPER() issue | No context = generic answer |
| Role prompt | Better — Snowflake-specific index advice | Persona drives domain depth |
| Chain of thought | Best — partition pruning analysis | Step by step = deeper reasoning |
| Few-shot | Consistent severity classification | Examples set the pattern |
| JSON output | Structured but is_efficient wrong | LLM output needs validation |

Key lesson: the JSON output had `is_efficient: true` which is
wrong — the query is NOT efficient. This demonstrates that LLM
outputs always need validation before being used in automated
pipelines. Never trust without checking.

## How this connects to my work experience
At Optum I produce data quality reports for stakeholders who are
not technical. The dbt_report_summariser.py automates exactly
that — converting dbt test JSON into a business-readable report
in seconds. This could save hours of manual reporting every week.

Using Ollama instead of a cloud API is directly relevant to
Optum's HIPAA requirements — patient data cannot be sent to
external APIs. Self-hosted LLMs like Llama 3.2 run inside the
corporate boundary, making AI-powered data tools compliant.

The prompt engineering techniques map directly to governance work:
output formatting (JSON) for automated pipeline triggers, role
prompting for domain-specific HIPAA/GDPR analysis, chain of
thought for complex data lineage investigations.

## Talking points
- "I built a pipeline that automatically converts dbt test results
  into plain English business reports using a local LLM. Runs after
  every CI/CD pipeline execution and gives the Head of Data an
  executive summary, risk level, and recommended action — no manual
  interpretation needed."
- "For Optum's HIPAA environment I use Ollama — LLMs running locally
  so patient data never leaves the corporate boundary. Same
  capability as cloud APIs, fully compliant."
- "Prompt engineering is as important as model choice — role
  prompting plus chain of thought on the same question produces
  dramatically better output than zero-shot."
- "LLM outputs always need validation in automated pipelines —
  I learned this when the JSON output had is_efficient=true for
  a clearly inefficient query. Trust but verify."
- "Token usage monitoring is essential in production — LLM costs
  scale with usage exactly like Snowflake compute costs. Ollama
  eliminates this concern for on-premise deployments."

## Errors I hit and how I fixed them

| Error | Cause | Fix |
|---|---|---|
| Pasted Python code into terminal | Misread theory section as executable code | Theory sections are reading only — only run .py files |
| google.generativeai deprecated warning | Google moved to new google.genai package | Switched to pip install google-genai |
| 429 RESOURCE_EXHAUSTED gemini-2.0-flash | Free tier quota limit=0 for this model | Tried gemini-flash-latest alias |
| All Gemini models quota exhausted | Daily free tier limit hit across all models | Switched to Ollama local LLM entirely |
| ModuleNotFoundError: ollama | Python Ollama library not installed separately from Ollama app | pip install ollama |
| zstd missing during Ollama install | Ubuntu missing compression library | sudo apt-get install zstd first then rerun install |
| ModuleNotFoundError: dotenv | python-dotenv not installed | pip install python-dotenv |
| protobuf version conflict | google-generativeai needs protobuf<6 but dbt needs protobuf>=6 | pip install protobuf>=6.0,<7.0 to satisfy dbt |

## Resources
- Ollama: ollama.com
- Ollama Python library: github.com/ollama/ollama-python
- Llama 3.2 model: ollama.com/library/llama3.2
- Google AI Stud
