import chromadb
from sentence_transformers import SentenceTransformer
import ollama
import os

print("Initialising RAG pipeline...")
print("=" * 60)

# ── Step 1: Load documents ────────────────────────────────────
print("\nStep 1: Loading documents...")

docs_folder = "documents"
documents = []
doc_names = []

for filename in os.listdir(docs_folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(docs_folder, filename)
        with open(filepath, "r") as f:
            content = f.read()
            documents.append(content)
            doc_names.append(filename)
        print(f"  Loaded: {filename} ({len(content)} characters)")

print(f"  Total documents loaded: {len(documents)}")

# ── Step 2: Chunk documents ───────────────────────────────────
print("\nStep 2: Chunking documents...")

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

all_chunks = []
all_chunk_ids = []
all_metadata = []

for doc_idx, (doc, name) in enumerate(zip(documents, doc_names)):
    chunks = chunk_text(doc)
    for chunk_idx, chunk in enumerate(chunks):
        all_chunks.append(chunk)
        all_chunk_ids.append(f"{name}_chunk_{chunk_idx}")
        all_metadata.append({"source": name, "chunk": chunk_idx})

print(f"  Total chunks created: {len(all_chunks)}")

# ── Step 3: Generate embeddings ───────────────────────────────
print("\nStep 3: Generating embeddings...")
print("  Loading sentence transformer model...")

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = embedding_model.encode(all_chunks).tolist()

print(f"  Embeddings generated: {len(embeddings)}")
print(f"  Embedding dimensions: {len(embeddings[0])}")

# ── Step 4: Store in ChromaDB ─────────────────────────────────
print("\nStep 4: Storing in ChromaDB vector database...")

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="company_docs",
    metadata={"hnsw:space": "cosine"}
)

collection.add(
    documents=all_chunks,
    embeddings=embeddings,
    ids=all_chunk_ids,
    metadatas=all_metadata
)

print(f"  Stored {collection.count()} chunks in ChromaDB")

# ── Query function ────────────────────────────────────────────
def ask_question(question):
    print(f"\n{'='*60}")
    print(f"QUESTION: {question}")
    print(f"{'='*60}")

    # embed the question
    question_embedding = embedding_model.encode([question]).tolist()

    # search for similar chunks
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=3
    )

    # get retrieved context
    retrieved_chunks = results['documents'][0]
    retrieved_sources = [m['source'] for m in results['metadatas'][0]]

    print(f"\nRetrieved {len(retrieved_chunks)} relevant chunks from:")
    for source in set(retrieved_sources):
        print(f"  - {source}")

    # build context for LLM
    context = "\n\n---\n\n".join(retrieved_chunks)

    prompt = f"""You are a helpful data engineering assistant.
Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I don't have that
information in the documentation."

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

    # call LLM with retrieved context
    response = ollama.chat(
        model='llama3.2',
        messages=[
            {
                'role': 'system',
                'content': """You are a precise data engineering
                assistant. Answer only from the provided context.
                Be concise and accurate."""
            },
            {'role': 'user', 'content': prompt}
        ]
    )

    print(f"\nANSWER:")
    print(response['message']['content'])
    print(f"\nSources used: {set(retrieved_sources)}")

# ── Test with real questions ──────────────────────────────────
print("\n" + "="*60)
print("RAG PIPELINE READY — Testing with questions")
print("="*60)

ask_question("What columns does the customers dbt model have?")
ask_question("What are the GDPR requirements for data erasure requests?")
ask_question("What is the Snowflake account identifier for our environment?")
ask_question("What are the data retention policies for customer data?")
ask_question("What tests are applied to the raw_orders source?")
