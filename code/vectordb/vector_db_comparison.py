print("Vector Database Comparison — 2026")
print("=" * 60)

comparison = {
    "ChromaDB": {
        "type": "Open source, embedded",
        "deployment": "Local or server",
        "cost": "Free",
        "best_for": "Learning, prototyping, small projects",
        "scale": "Millions of vectors",
        "features": ["Simple API", "Local storage", "Metadata filtering"],
        "used_in": "Day 9 and Day 10 of this project",
    },
    "Pinecone": {
        "type": "Managed cloud service",
        "deployment": "Cloud only",
        "cost": "Free tier then paid",
        "best_for": "Production, enterprise, no ops overhead",
        "scale": "Billions of vectors",
        "features": ["Managed", "Hybrid search", "Namespaces", "High availability"],
        "used_in": "Most common in enterprise RAG pipelines",
    },
    "Weaviate": {
        "type": "Open source or managed",
        "deployment": "Self-hosted or cloud",
        "cost": "Free (self-hosted) or paid (cloud)",
        "best_for": "Multi-modal search, GraphQL API",
        "scale": "Billions of vectors",
        "features": ["GraphQL", "Multi-modal", "Hybrid search", "Modules"],
        "used_in": "Enterprise with complex search requirements",
    },
    "pgvector": {
        "type": "PostgreSQL extension",
        "deployment": "Wherever Postgres runs",
        "cost": "Free",
        "best_for": "Teams already using PostgreSQL",
        "scale": "Hundreds of millions of vectors",
        "features": ["SQL interface", "ACID", "Existing Postgres tooling"],
        "used_in": "Supabase, Railway, any Postgres deployment",
    },
    "Snowflake (VECTOR type)": {
        "type": "Native warehouse feature",
        "deployment": "Snowflake cloud",
        "cost": "Snowflake compute costs",
        "best_for": "Teams already on Snowflake, SQL-first teams",
        "scale": "Enterprise scale",
        "features": ["Native SQL", "No separate service", "Cortex integration"],
        "used_in": "Snowflake Cortex Search, enterprise AI",
    },
}

for db_name, details in comparison.items():
    print(f"\n{'='*60}")
    print(f"  {db_name}")
    print(f"{'='*60}")
    print(f"  Type:       {details['type']}")
    print(f"  Deployment: {details['deployment']}")
    print(f"  Cost:       {details['cost']}")
    print(f"  Scale:      {details['scale']}")
    print(f"  Best for:   {details['best_for']}")
    print(f"  Features:   {', '.join(details['features'])}")
    print(f"  Used in:    {details['used_in']}")

print("\n" + "="*60)
print("DECISION FRAMEWORK")
print("="*60)
print("""
Learning / Prototyping     → ChromaDB (free, simple, local)
Already on PostgreSQL      → pgvector (no new service needed)
Already on Snowflake       → Snowflake VECTOR type + Cortex
Need managed cloud service → Pinecone (most mature)
Complex multi-modal search → Weaviate
HIPAA / no cloud allowed   → ChromaDB or pgvector (self-hosted)

For your Optum context:
→ pgvector on internal Postgres OR
→ Snowflake VECTOR type (already have Snowflake)
→ Both keep data inside corporate boundary
→ Both use SQL interface your team already knows
""")
