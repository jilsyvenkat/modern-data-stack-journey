import chromadb
from sentence_transformers import SentenceTransformer
import ollama
import json
import os

print("RAG over real dbt documentation")
print("=" * 60)

# load real dbt manifest if it exists
manifest_path = "/mnt/c/Users/Venkat/jaffle_shop/target/manifest.json"

if os.path.exists(manifest_path):
    print(f"Loading real dbt manifest from {manifest_path}")
    with open(manifest_path) as f:
        manifest = json.load(f)

    # extract model descriptions and SQL
    documents = []
    doc_ids = []

    for node_name, node in manifest.get('nodes', {}).items():
        if node.get('resource_type') == 'model':
            doc_text = f"""
MODEL: {node.get('name')}
Description: {node.get('description', 'No description')}
Schema: {node.get('schema')}
Database: {node.get('database')}
Materialization: {node.get('config', {}).get('materialized')}

SQL:
{node.get('raw_code', 'No SQL available')}
"""
            documents.append(doc_text)
            doc_ids.append(node_name)
            print(f"  Loaded model: {node.get('name')}")

else:
    print("dbt manifest not found — using sample documentation")
    documents = [
        """MODEL: customers
        This model combines customer data with order history.
        Primary key: customer_id
        Columns: customer_id, first_name, last_name,
        number_of_orders, first_order_date
        Source: raw_customers joined with raw_orders
        Tests: unique and not_null on customer_id""",
    ]
    doc_ids = ["customers_model"]

# generate embeddings and store
print("\nGenerating embeddings...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = embedding_model.encode(documents).tolist()

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("dbt_docs")
collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=doc_ids
)

print(f"Stored {collection.count()} dbt models in vector database")

# ask questions about your dbt project
questions = [
    "What does the customers model do?",
    "What is the primary key of the customers model?",
    "How is the customers model materialized?",
]

for question in questions:
    print(f"\n{'='*60}")
    print(f"Q: {question}")

    q_embedding = embedding_model.encode([question]).tolist()
    results = collection.query(query_embeddings=q_embedding, n_results=1)
    context = results['documents'][0][0]

    response = ollama.chat(
        model='llama3.2',
        messages=[{
            'role': 'user',
            'content': f"Context: {context}\n\nQuestion: {question}\n\nAnswer concisely:"
        }]
    )
    print(f"A: {response['message']['content']}")
