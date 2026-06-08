"""
query.py — Grounded generation using retrieved chunks and Groq.

Retrieves the top 5 relevant chunks from ChromaDB, then sends them to
Groq's LLM as context. The model is instructed to answer ONLY from the
provided chunks — no outside knowledge allowed.

Run:
    python query.py
"""

import os
from dotenv import load_dotenv
from groq import Groq

from retrieve import build_vector_store, retrieve

# ── Load API key from .env ─────────────────────────────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL   = "llama-3.3-70b-versatile"

# ── System prompt — enforces grounding ────────────────────────────────────────
SYSTEM_PROMPT = """\
You are a helpful assistant for students at the University at Buffalo (UB) \
studying Computer Science. You answer questions using ONLY the context \
passages provided below each question.

Rules you must follow:
1. Base your answer exclusively on the provided context passages.
2. Do not use any outside knowledge, even if you have it.
3. If the context does not contain enough information to answer the question, \
respond with exactly: \
"I don't have enough information from the documents to answer that."
4. Keep your answer concise and directly relevant to the question.
"""


# ── ask ────────────────────────────────────────────────────────────────────────
def ask(question: str, collection, model) -> dict:
    """
    Retrieve relevant chunks, build a grounded prompt, and call Groq.

    Returns a dict with:
        answer   — the model's response
        sources  — list of {source_file, chunk_index} for each chunk used
    """
    # Step 1: retrieve the top 5 chunks for this question
    chunks = retrieve(question, collection, model, top_k=5)

    # Step 2: build a numbered context block from the chunks
    context_lines = []
    for i, chunk in enumerate(chunks, start=1):
        context_lines.append(
            f"[{i}] (source: {chunk['source_file']}, chunk {chunk['chunk_index']})\n"
            f"{chunk['text']}"
        )
    context_block = "\n\n".join(context_lines)

    # Step 3: assemble the user message — question + context
    user_message = f"""\
Question: {question}

Context passages:
{context_block}
"""

    # Step 4: call Groq
    client   = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        temperature=0.0,   # deterministic — we want factual, grounded answers
    )

    answer = response.choices[0].message.content.strip()

    # Step 5: collect the sources that were passed to the model
    sources = [
        {"source_file": c["source_file"], "chunk_index": c["chunk_index"]}
        for c in chunks
    ]

    return {"answer": answer, "sources": sources}


# ── Test section ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Load the vector store once — reused for all queries
    print("Initializing vector store...")
    collection, embed_model = build_vector_store()

    test_questions = [
        "What do students say about CSE 250?",
        "How should I prepare for CSE 116 and CSE 191?",
        "What is the best dining hall at UB?",   # out-of-scope — should refuse
    ]

    for question in test_questions:
        print(f"\n{'=' * 70}")
        print(f"Question: {question}")
        print("=" * 70)

        result = ask(question, collection, embed_model)

        print(f"\nAnswer:\n{result['answer']}")

        print("\nSources used:")
        for s in result["sources"]:
            print(f"  - {s['source_file']}  (chunk {s['chunk_index']})")
