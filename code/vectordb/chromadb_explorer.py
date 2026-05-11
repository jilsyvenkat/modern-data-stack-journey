import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

print("ChromaDB Deep Dive")
print("=" * 60)

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.Client()

# ── Part 1: Understand embeddings ─────────────────────────────
print("\nPART 1: Understanding embeddings")
print("-" * 40)

sentences = [
    "The customers dbt model has a primary key on customer_id",
    "Our data model stores one record per customer with order history",
    "The raw_orders table contains transaction records",
    "GDPR requires data erasure within 30 days of request",
    "What is the weather like in Dublin today?",
]

embeddings = embedding_model.encode(sentences)

print(f"Embedding dimensions: {embeddings.shape[1]}")
print(f"Each sentence becomes {embeddings.shape[1]} numbers\n")

# calculate similarity between pairs
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

reference = embeddings[0]
print(f"Reference: '{sentences[0][:50]}...'")
print(f"{'='*60}")
for i, (sentence, embedding) in enumerate(zip(sentences[1:], embeddings[1:]), 1):
    similarity = cosine_similarity(reference, embedding)
    bar = "█" * int(similarity * 20)
    print(f"Similarity: {similarity:.3f} {bar}")
    print(f"  '{sentence[:60]}'")
    print()

# ── Part 2: ChromaDB collections ──────────────────────────────
print("\nPART 2: ChromaDB collections")
print("-" * 40)

collection = chroma_client.get_or_create_collection(
    name="data_knowledge",
    metadata={"hnsw:space": "cosine"}
)

# add documents with metadata
data_docs = [
    {
        "id": "doc_001",
        "text": "The customers model combines raw customer data with order history producing one row per customer with customer_id as primary key",
        "metadata": {"category": "dbt", "topic": "models", "day": "1"}
    },
    {
        "id": "doc_002",
        "text": "Snowflake Time Travel allows querying data as it existed at any past point using AT OFFSET or AT TIMESTAMP syntax",
        "metadata": {"category": "snowflake", "topic": "time_travel", "day": "2"}
    },
    {
        "id": "doc_003",
        "text": "Apache Kafka uses topics and partitions to store event streams with consumers tracking position using offsets",
        "metadata": {"category": "kafka", "topic": "architecture", "day": "3"}
    },
    {
        "id": "doc_004",
        "text": "Apache Airflow DAGs define task dependencies using the >> operator ensuring tasks run in correct sequence",
        "metadata": {"category": "airflow", "topic": "dags", "day": "4"}
    },
    {
        "id": "doc_005",
        "text": "Delta Lake provides ACID transactions on data lakes with time travel using version numbers and transaction logs",
        "metadata": {"category": "delta", "topic": "acid", "day": "5"}
    },
    {
        "id": "doc_006",
        "text": "dbt tests include unique not_null accepted_values and relationships defined in schema.yml files",
        "metadata": {"category": "dbt", "topic": "testing", "day": "6"}
    },
    {
        "id": "doc_007",
        "text": "RAG combines document retrieval with LLM generation grounding answers in your own documents using vector similarity search",
        "metadata": {"category": "ai", "topic": "rag", "day": "9"}
    },
    {
        "id": "doc_008",
        "text": "GDPR requires data erasure within 30 days right to access within 30 days and data minimisation principles",
        "metadata": {"category": "governance", "topic": "gdpr", "day": "6"}
    },
    {
        "id": "doc_009",
        "text": "Apache Iceberg supports schema evolution adding columns without rewriting data using metadata only changes",
        "metadata": {"category": "iceberg", "topic": "schema", "day": "5"}
    },
    {
        "id": "doc_010",
        "text": "Ollama runs LLMs locally with no API cost suitable for HIPAA environments where data cannot leave corporate boundary",
        "metadata": {"category": "ai", "topic": "ollama", "day": "8"}
    },
]

doc_embeddings = embedding_model.encode(
    [d["text"] for d in data_docs]
).tolist()

collection.add(
    documents=[d["text"] for d in data_docs],
    embeddings=doc_embeddings,
    ids=[d["id"] for d in data_docs],
    metadatas=[d["metadata"] for d in data_docs]
)

print(f"Added {collection.count()} documents to ChromaDB")

# ── Part 3: Different types of search ─────────────────────────
print("\nPART 3: Semantic search examples")
print("-" * 40)

queries = [
    ("How do I undo a mistake in my data?",          None),
    ("What tools handle real-time data streams?",    None),
    ("How do I ensure data quality?",                None),
    ("privacy and compliance requirements",          {"category": "governance"}),
    ("AI tools for data engineering",               {"category": "ai"}),
]

for query, where_filter in queries:
    print(f"\nQuery: '{query}'")
    if where_filter:
        print(f"Filter: {where_filter}")

    q_embedding = embedding_model.encode([query]).tolist()

    if where_filter:
        results = collection.query(
            query_embeddings=q_embedding,
            n_results=2,
            where=where_filter
        )
    else:
        results = collection.query(
            query_embeddings=q_embedding,
            n_results=2
        )

    for doc, meta, distance in zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    ):
        similarity = 1 - distance
        print(f"  [{similarity:.3f}] [{meta['category']}] {doc[:70]}...")

# ── Part 4: Metadata filtering ────────────────────────────────
print("\n\nPART 4: Metadata filtering")
print("-" * 40)

# filter by day learned
for day in ["1", "5", "9"]:
    results = collection.get(where={"day": day})
    print(f"Day {day} topics: {[m['topic'] for m in results['metadatas']]}")

print("\n" + "="*60)
print("KEY INSIGHTS")
print("="*60)
print("""
1. Embeddings capture MEANING not just words
   "undo a mistake" → found Time Travel (correct!)
   "real-time streams" → found Kafka (correct!)
   "data quality" → found dbt testing (correct!)

2. Metadata filtering narrows the search space
   Filter by category/day/topic before vector search
   Combine semantic search with structured filters

3. Distance vs similarity
   ChromaDB returns distance (lower = more similar)
   Similarity = 1 - distance (higher = more similar)
   Threshold: similarity > 0.7 usually means relevant
""")
