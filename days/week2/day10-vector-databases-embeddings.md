# Day 10 — Vector databases & embeddings in depth

## What I learned today
Went deep on how embeddings work mathematically — vectors of 384
numbers capturing semantic meaning, with cosine similarity measuring
how close two meanings are. Built three scripts: a ChromaDB explorer
demonstrating similarity scores and metadata filtering, a vector
database comparison covering ChromaDB vs Pinecone vs Weaviate vs
pgvector vs Snowflake VECTOR type, and a semantic search engine
over all 9 days of learning notes.

## Key concepts

- **Embedding dimensions** — all-MiniLM-L6-v2 produces 384 numbers
  per text. Larger models produce more dimensions (1536 for
  OpenAI ada-002) — more dimensions = more nuanced similarity
  but more storage and compute cost.

- **Cosine similarity** — measures angle between two vectors.
  1.0 = identical meaning. 0.0 = unrelated. Negative = opposite.
  Production threshold: similarity > 0.7 usually means relevant.

- **Semantic search** — finds documents by meaning not keywords.
  "undo a mistake" finds Time Travel documentation.
  "real-time streams" finds Kafka documentation.
  SQL LIKE cannot do this.

- **Metadata filtering** — combine vector search with structured
  filters. Filter by category, date, author before searching
  by meaning. Dramatically improves precision.

- **HNSW index** — Hierarchical Navigable Small World graph.
  The algorithm ChromaDB and most vector DBs use for fast
  approximate nearest neighbour search at scale.

## What I built today

- **chromadb_explorer.py** — 10 documents from 21-day journey
  stored in ChromaDB. Demonstrated cosine similarity scores,
  semantic search finding correct topics from natural questions,
  and metadata filtering by category and day.

- **vector_db_comparison.py** — comparison of 5 vector database
  options with decision framework for different scenarios.
  Key insight: for Optum's HIPAA environment, pgvector or
  Snowflake VECTOR type keeps data inside corporate boundary.

- **semantic_search_notes.py** — semantic search engine over
  all 9 days of learning notes. Ask natural language questions
  and get AI-synthesised answers from your actual documentation.

## Similarity scores from chromadb_explorer

Query: "How do I undo a mistake in my data?"
→ Found: Snowflake Time Travel (correct — highest similarity)

Query: "What tools handle real-time data streams?"
→ Found: Apache Kafka (correct)

Query: "How do I ensure data quality?"
→ Found: dbt testing (correct)

The model has never seen these exact questions but finds the
right answers through semantic similarity. This is the power
of embeddings.

## Vector database decision framework

| Scenario | Recommended DB | Reason |
|----------|---------------|--------|
| Learning / prototyping | ChromaDB | Free, simple, local |
| Already on PostgreSQL | pgvector | No new service needed |
| Already on Snowflake | Snowflake VECTOR | SQL interface, no new service |
| Production managed | Pinecone | Most mature, no ops overhead |
| Multi-modal search | Weaviate | Best GraphQL and module support |
| HIPAA / no cloud | ChromaDB or pgvector | Self-hosted, data stays local |

## How this connects to my work experience
At Optum the semantic search engine built today has direct
application — searching HIPAA policies, data governance
documents, and pipeline documentation by meaning rather than
keyword. A data analyst asking "what are the retention rules
for patient data?" gets the right policy section instantly
without knowing the exact terminology.

The pgvector recommendation is directly relevant — Optum likely
already has PostgreSQL infrastructure. Adding vector search to
existing Postgres is a low-friction way to add AI search
capability without new infrastructure or data leaving the
corporate boundary.

## Talking points
- "Embeddings capture semantic meaning as vectors — similar
  meaning produces similar vectors regardless of exact wording.
  This enables search that SQL LIKE cannot do."
- "For Optum's HIPAA environment I would use pgvector or
  Snowflake VECTOR type — both keep data inside the corporate
  boundary and use SQL interfaces my team already knows."
- "Metadata filtering combined with vector search dramatically
  improves precision — filter by document type or date first,
  then search by semantic similarity within that subset."
- "I built a semantic search engine over our entire data
  engineering documentation — analysts find relevant policies
  and pipeline docs by asking natural language questions."

## Errors I hit and how I fixed them

| Error | Cause | Fix |
|---|---|---|
| Add yours here | | |

## Resources
- ChromaDB docs: docs.trychroma.com
- pgvector: github.com/pgvector/pgvector
- Pinecone docs: docs.pinecone.io
- Weaviate docs: weaviate.io/developers/weaviate
- Snowflake VECTOR: docs.snowflake.com/en/sql-reference/data-types-vector
- My code: /code/vectordb/
