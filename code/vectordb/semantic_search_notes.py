import chromadb
from sentence_transformers import SentenceTransformer
import ollama
import os
import glob

print("Semantic Search Engine — Modern Data Stack Journey")
print("=" * 60)

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(
    name="learning_notes",
    metadata={"hnsw:space": "cosine"}
)

# load all your day notes
notes_path = "/mnt/c/Users/Venkat/modern-data-stack-journey/days"
all_files = glob.glob(f"{notes_path}/**/*.md", recursive=True)

print(f"\nFound {len(all_files)} note files")

documents = []
doc_ids = []
metadatas = []

for filepath in all_files:
    with open(filepath, 'r') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    day_num = filename.split('-')[0].replace('day', '')

    # chunk by sections
    sections = content.split('\n## ')
    for i, section in enumerate(sections):
        if len(section.strip()) > 100:
            documents.append(section[:800])
            doc_ids.append(f"{filename}_section_{i}")
            metadatas.append({
                "file": filename,
                "day": day_num,
                "section": i
            })

print(f"Created {len(documents)} searchable chunks from your notes")

if documents:
    embeddings = embedding_model.encode(documents).tolist()
    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=doc_ids,
        metadatas=metadatas
    )
    print(f"Stored in ChromaDB — ready to search!")

# semantic search function
def search_notes(query, use_llm=True):
    print(f"\n{'='*60}")
    print(f"SEARCH: {query}")
    print(f"{'='*60}")

    q_embedding = embedding_model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=q_embedding,
        n_results=3
    )

    print(f"\nTop matches from your notes:")
    context_parts = []
    for doc, meta, distance in zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    ):
        similarity = 1 - distance
        print(f"  [{similarity:.3f}] {meta['file']} — section {meta['section']}")
        context_parts.append(doc)

    if use_llm and context_parts:
        context = "\n\n".join(context_parts)
        response = ollama.chat(
            model='llama3.2',
            messages=[{
                'role': 'user',
                'content': f"""Based on these learning notes:

{context}

Answer this question concisely: {query}"""
            }]
        )
        print(f"\nAI Summary:")
        print(response['message']['content'][:500])

# test searches
search_notes("How does dbt handle data lineage?")
search_notes("What is the difference between Kafka and Airflow?")
search_notes("How do I handle GDPR compliance in Snowflake?")
search_notes("What errors did I hit with Airflow?")
