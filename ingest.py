"""
ingest.py — Load, clean, chunk, and save raw documents.
Produces documents/chunks/chunks.json for later use in the RAG pipeline.
"""

import json
import re
from pathlib import Path

# ── Configuration ─────────────────────────────────────────────────────────────
RAW_DIR    = Path("documents/raw")       # folder with source .txt files
CHUNKS_DIR = Path("documents/chunks")   # folder where output will be saved
CHUNK_SIZE = 700                         # target characters per chunk
OVERLAP    = 150                         # characters of overlap between chunks


# ── Step 1: Load a file and split off the TEXT: section ───────────────────────
def load_document(filepath: Path) -> str:
    """Read a file and return only the text that follows 'TEXT:'."""
    raw = filepath.read_text(encoding="utf-8")

    # Everything after "TEXT:" is the content we want
    if "TEXT:" in raw:
        text = raw.split("TEXT:", 1)[1]
    else:
        text = raw  # fall back to the whole file if marker is missing

    return text


# ── Step 2: Clean the text ─────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    """Remove extra whitespace and collapse repeated blank lines."""
    # Replace any run of whitespace (tabs, multiple spaces) with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Collapse three or more newlines down to two (one blank line)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ── Step 3: Split text into overlapping chunks ────────────────────────────────
def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    """
    Split text into chunks of ~chunk_size characters.
    Each chunk overlaps the previous one by ~overlap characters.
    Word boundaries are respected so we never cut a word in half.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        if end >= len(text):
            # We've reached the end — grab the remainder
            chunks.append(text[start:].strip())
            break

        # Walk backward from end until we find a space (word boundary)
        while end > start and text[end] not in (" ", "\n"):
            end -= 1

        # If no space was found (very long word), just cut at chunk_size
        if end == start:
            end = start + chunk_size

        chunks.append(text[start:end].strip())

        # Next chunk starts overlap characters before the current end
        start = end - overlap

        # Walk forward to the next word boundary so the overlap starts cleanly
        while start < len(text) and text[start] not in (" ", "\n"):
            start += 1
        start += 1  # skip past the space itself

    # Remove any empty strings that slipped through
    return [c for c in chunks if c]


# ── Step 4: Main pipeline ─────────────────────────────────────────────────────
def main():
    # Make sure the output folder exists
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    all_chunks = []
    chunk_id   = 0

    txt_files = sorted(RAW_DIR.glob("*.txt"))
    print(f"Documents loaded: {len(txt_files)}")

    for filepath in txt_files:
        # Load and clean this document
        raw_text     = load_document(filepath)
        cleaned_text = clean_text(raw_text)

        # Split into chunks
        text_chunks = chunk_text(cleaned_text)

        # Build a record for each chunk
        for chunk_index, chunk_text_content in enumerate(text_chunks):
            all_chunks.append({
                "chunk_id":    chunk_id,
                "source_file": filepath.name,
                "chunk_index": chunk_index,
                "text":        chunk_text_content,
            })
            chunk_id += 1

    print(f"Total chunks created: {len(all_chunks)}")

    # ── Save to JSON ──────────────────────────────────────────────────────────
    output_path = CHUNKS_DIR / "chunks.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"Saved to {output_path}\n")

    # ── Print 5 sample chunks ─────────────────────────────────────────────────
    print("── 5 Sample Chunks ──────────────────────────────────────────────────")
    for sample in all_chunks[:5]:
        print(f"\nchunk_id    : {sample['chunk_id']}")
        print(f"source_file : {sample['source_file']}")
        print(f"chunk_index : {sample['chunk_index']}")
        print(f"text        : {sample['text'][:200]}{'...' if len(sample['text']) > 200 else ''}")
        print("-" * 70)


if __name__ == "__main__":
    main()
