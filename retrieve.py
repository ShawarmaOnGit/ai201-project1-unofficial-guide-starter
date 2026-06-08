"""
retrieve.py — Embed chunks into ChromaDB and retrieve relevant chunks for a query.

Uses sentence-transformers with all-MiniLM-L6-v2.

Run:
    python retrieve.py
"""

import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# ── Configuration ──────────────────────────────────────────────────────────────
CHUNKS_FILE = Path("documents/chunks/chunks.json")
CHROMA_DIR  = Path("documents/chroma_db")   # ChromaDB saves its files here
COLLECTION  = "ub_cs_guide"                  # name of the collection inside ChromaDB
EMBED_MODEL = "all-MiniLM-L6-v2"            # sentence-transformers model name


# ── build_vector_store ─────────────────────────────────────────────────────────
def build_vector_store():
    """
    Read chunks.json, embed each chunk, and store everything in ChromaDB.
    Safe to call multiple times — skips loading if the collection already has data.
    Returns the collection and the loaded model.
    """
    # Load the embedding model (downloads once, then cached locally)
    print("Loading embedding model...")
    model = SentenceTransformer(EMBED_MODEL)

    # Connect to (or create) a persistent ChromaDB on disk
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Get or create the collection
    collection = client.get_or_create_collection(name=COLLECTION)

    # Skip rebuilding if we already have data
    if collection.count() > 0:
        print(f"Vector store already contains {collection.count()} chunks. Skipping rebuild.")
        return collection, model

    # Load chunks from JSON
    print("Loading chunks from JSON...")
    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
    print(f"Loaded {len(chunks)} chunks.")

    # Build lists that ChromaDB expects
    ids        = []   # unique string ID for each chunk
    documents  = []   # the raw text
    metadatas  = []   # extra info stored alongside each vector
    embeddings = []   # the actual vectors we compute ourselves

    print("Embedding chunks (this may take a moment)...")
    for chunk in chunks:
        vector = model.encode(chunk["text"]).tolist()  # compute embedding
        ids.append(str(chunk["chunk_id"]))
        documents.append(chunk["text"])
        metadatas.append({
            "source_file": chunk["source_file"],
            "chunk_index": chunk["chunk_index"],
        })
        embeddings.append(vector)

    # Add everything to ChromaDB
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print(f"Stored {collection.count()} chunks in ChromaDB.")
    return collection, model


# ── retrieve ───────────────────────────────────────────────────────────────────
def retrieve(query: str, collection, model, top_k: int = 5) -> list[dict]:
    """
    Embed the query and return the top_k most similar chunks from ChromaDB.

    Returns a list of dicts, each with:
        text, source_file, chunk_index, distance
    """
    # Embed the query with the same model used during ingestion
    query_vector = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    # Repack into a clean list of dicts
    chunks = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text":        text,
            "source_file": meta["source_file"],
            "chunk_index": meta["chunk_index"],
            "distance":    round(dist, 4),
        })

    return chunks


# ── Test section ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Build (or load) the vector store
    collection, model = build_vector_store()

    # Test queries
    test_queries = [
        "What do students say about CSE 250?",
        "How should I prepare for CSE 116 and CSE 191?",
        "What advice do students give about getting internships?",
    ]

    for query in test_queries:
        print(f"\n{'=' * 70}")
        print(f"Query: {query}")
        print("=" * 70)

        results = retrieve(query, collection, model)

        for i, chunk in enumerate(results, start=1):
            print(f"\n  Result {i}")
            print(f"  Source : {chunk['source_file']}  (chunk {chunk['chunk_index']})")
            print(f"  Score  : {chunk['distance']}  (lower = more similar)")
            print(f"  Text   : {chunk['text'][:300]}{'...' if len(chunk['text']) > 300 else ''}")
