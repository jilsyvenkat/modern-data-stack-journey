import ollama

def call_llm(system, user_message, label):
    response = ollama.chat(
        model='llama3.2',
        messages=[
            {'role': 'system',  'content': system},
            {'role': 'user',    'content': user_message}
        ]
    )
    print(f"\n{'='*60}")
    print(f"TECHNIQUE: {label}")
    print(f"{'='*60}")
    print(response['message']['content'])

sql_question = "Is this SQL query efficient? SELECT * FROM orders WHERE UPPER(status) = 'COMPLETED'"

# ── Technique 1 — Zero-shot ───────────────────────────────────
call_llm(
    system="You are a data engineering expert.",
    user_message=sql_question,
    label="1. Zero-shot — no examples given"
)

# ── Technique 2 — Role prompting ─────────────────────────────
call_llm(
    system="""You are a senior Snowflake performance engineer with
    15 years experience optimising enterprise data warehouses.
    You give specific actionable advice with SQL examples.
    Always show the improved query.""",
    user_message=sql_question,
    label="2. Role prompting — specific expert persona"
)

# ── Technique 3 — Chain of thought ───────────────────────────
call_llm(
    system="You are a data engineering expert.",
    user_message=f"""{sql_question}

    Think through this step by step:
    1. What does UPPER() do to query performance?
    2. Can Snowflake use partition pruning here?
    3. What is the recommended fix?
    4. Show the improved query.""",
    label="3. Chain of thought — step by step reasoning"
)

# ── Technique 4 — Few-shot ────────────────────────────────────
call_llm(
    system="You are a data engineering expert.",
    user_message="""Classify these SQL patterns by severity.

    Examples:
    SELECT * FROM large_table → HIGH severity
    (reads all columns, wastes memory and compute)

    SELECT id FROM orders WHERE id > 0 → LOW severity
    (simple filter on indexed column, efficient)

    Now classify these:
    1. SELECT * FROM orders WHERE UPPER(status) = 'COMPLETED'
    2. SELECT COUNT(*) FROM orders
    3. SELECT * FROM orders o JOIN customers c
       ON UPPER(o.customer_id) = UPPER(c.id)""",
    label="4. Few-shot — examples provided before the task"
)

# ── Technique 5 — Output formatting ──────────────────────────
call_llm(
    system="You are a data engineering expert. Respond only with valid JSON. No explanation, no markdown.",
    user_message=f"""Analyse this SQL query and respond ONLY with JSON.

    Query: SELECT * FROM orders WHERE UPPER(status) = 'COMPLETED'

    JSON format:
    {{
        "is_efficient": true or false,
        "issues": ["list of issues"],
        "severity": "LOW or MEDIUM or HIGH",
        "improved_query": "the better SQL",
        "performance_gain": "estimated improvement"
    }}""",
    label="5. Output formatting — structured JSON response"
)

print("\n" + "="*60)
print("PROMPT ENGINEERING SUMMARY")
print("="*60)
print("""
Techniques demonstrated:
1. Zero-shot      — just ask, no context
2. Role prompt    — specific expert persona
3. Chain of thought — reason step by step
4. Few-shot       — examples before the task
5. Output format  — structured JSON response

Key insight: same question, five different prompts,
five dramatically different quality answers.
Role prompting + chain of thought gives the best
results for data engineering use cases.
""")
