from pathlib import Path
import json
import re
import html
import random

DOCUMENTS_DIR = Path("documents")
OUTPUT_FILE = Path("chunks.json")

MIN_CHUNK_SIZE = 700
MAX_CHUNK_SIZE = 900
OVERLAP = 100


def clean_text(text: str) -> str:
    """Clean copied article/thread text before chunking."""
    text = html.unescape(text)

    # Remove HTML tags if copied text includes them.
    text = re.sub(r"<[^>]+>", " ", text)

    # Normalize whitespace.
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove common web junk.
    junk_phrases = [
        "Accept all cookies",
        "Cookie settings",
        "Subscribe to our newsletter",
        "Sign up to continue",
        "Share this article",
        "Read more",
        "Advertisement",
    ]

    for phrase in junk_phrases:
        text = re.sub(re.escape(phrase), " ", text, flags=re.IGNORECASE)

    return text.strip()


def parse_document(path: Path) -> dict:
    """
    Expected format:

    Title: Example Source Title
    URL: https://example.com

    ---

    Main copied text here.
    """
    raw = path.read_text(encoding="utf-8")

    title = path.stem
    url = ""

    title_match = re.search(r"^Title:\s*(.+)$", raw, flags=re.MULTILINE)
    url_match = re.search(r"^URL:\s*(.+)$", raw, flags=re.MULTILINE)

    if title_match:
        title = title_match.group(1).strip()

    if url_match:
        url = url_match.group(1).strip()

    if "---" in raw:
        body = raw.split("---", 1)[1]
    else:
        body = raw

    return {
        "source_file": path.name,
        "title": title,
        "url": url,
        "text": clean_text(body),
    }


def split_units(text: str) -> list[str]:
    """
    Prefer paragraph-level units.
    If a document has no paragraph breaks, fall back to sentence-like units.
    """
    text = text.replace("\n---\n", "\n\n---COMMENT BREAK---\n\n")
    units = [p.strip() for p in text.split("\n\n") if p.strip()]

    if len(units) <= 1:
        units = re.split(r"(?<=[.!?])\s+", text)
        units = [u.strip() for u in units if u.strip()]

    return units


def split_long_text(text: str, max_size: int = MAX_CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    """Split a long paragraph into overlapping character chunks."""
    pieces = []
    start = 0

    while start < len(text):
        end = start + max_size
        piece = text[start:end].strip()

        if piece:
            pieces.append(piece)

        if end >= len(text):
            break

        start = end - overlap

    return pieces

def get_overlap_text(text: str, overlap: int) -> str:
    """Return overlap text without starting in the middle of a word."""
    if len(text) <= overlap:
        return text.strip()

    overlap_text = text[-overlap:]

    # Move start to first whitespace so we don't begin mid-word.
    first_space = overlap_text.find(" ")
    if first_space != -1:
        overlap_text = overlap_text[first_space + 1:]

    return overlap_text.strip()

def chunk_text(text: str) -> list[str]:
    """
    Paragraph-aware chunking:
    - target: 700–900 characters
    - overlap: 100 characters
    - preserve readable units when possible
    - avoid merging separate Reddit/forum comments
    """
    units = split_units(text)
    chunks = []
    current = ""

    for unit in units:
        if not unit.strip():
            continue

        # Treat comment separators as hard chunk boundaries.
        if unit == "---COMMENT BREAK---":
            if current.strip():
                chunks.append(current.strip())
                current = ""
            continue

        # If one paragraph/comment is too long, split it separately.
        if len(unit) > MAX_CHUNK_SIZE:
            if current.strip():
                chunks.append(current.strip())
                current = ""

            chunks.extend(split_long_text(unit))
            continue

        candidate = f"{current}\n\n{unit}".strip() if current else unit

        if len(candidate) <= MAX_CHUNK_SIZE:
            current = candidate
        else:
            if current.strip():
                chunks.append(current.strip())

            overlap_text = get_overlap_text(current, OVERLAP) if current else ""

            # Use overlap only if it does not make the new chunk too bloated.
            with_overlap = f"{overlap_text}\n\n{unit}".strip()
            if len(with_overlap) <= MAX_CHUNK_SIZE:
                current = with_overlap
            else:
                current = unit

    if current.strip():
        chunks.append(current.strip())

    # Remove useless tiny fragments.
    chunks = [chunk for chunk in chunks if len(chunk) >= 80]

    return chunks


def load_and_chunk_documents() -> list[dict]:
    txt_files = sorted(DOCUMENTS_DIR.glob("*.txt"))

    if not txt_files:
        raise FileNotFoundError(
            "No .txt files found in documents/. Add your source files first."
        )

    all_chunks = []

    for path in txt_files:
        doc = parse_document(path)
        chunks = chunk_text(doc["text"])

        for index, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{path.stem}_chunk_{index}",
                "text": chunk,
                "metadata": {
                    "source_file": doc["source_file"],
                    "title": doc["title"],
                    "url": doc["url"],
                    "chunk_index": index,
                    "char_count": len(chunk),
                }
            })

    return all_chunks


def print_sample_chunks(chunks: list[dict], sample_count: int = 5) -> None:
    print("\n--- 5 representative sample chunks ---\n")

    sample = random.sample(chunks, min(sample_count, len(chunks)))

    for chunk in sample:
        metadata = chunk["metadata"]

        print("=" * 80)
        print(f"Chunk ID: {chunk['id']}")
        print(f"Source: {metadata['title']}")
        print(f"URL: {metadata['url']}")
        print(f"Length: {metadata['char_count']} characters")
        print("-" * 80)
        print(chunk["text"])
        print()


def main():
    chunks = load_and_chunk_documents()

    OUTPUT_FILE.write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Loaded documents from: {DOCUMENTS_DIR}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Saved chunks to: {OUTPUT_FILE}")

    if len(chunks) < 50:
        print("Warning: fewer than 50 chunks. Your documents may be too short or chunks may be too large.")

    if len(chunks) > 2000:
        print("Warning: more than 2000 chunks. Your chunks may be too small.")

    print_sample_chunks(chunks)


if __name__ == "__main__":
    main()
