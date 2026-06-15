from pathlib import Path
import json
import textwrap

import chromadb
from sentence_transformers import SentenceTransformer


CHUNKS_FILE = Path("chunks.json")
CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "cs_portfolio_guide"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5


def load_chunks() -> list[dict]:
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError("chunks.json not found. Run `python src/ingest.py` first.")

    with CHUNKS_FILE.open("r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        raise ValueError("chunks.json is empty.")

    return chunks


def clean_metadata(metadata: dict) -> dict:
    """
    Chroma metadata values must be simple types.
    """
    cleaned = {}

    for key, value in metadata.items():
        if value is None:
            cleaned[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            cleaned[key] = value
        else:
            cleaned[key] = str(value)

    return cleaned


def build_vector_store(reset: bool = True):
    chunks = load_chunks()

    print(f"Loaded {len(chunks)} chunks.")
    print(f"Loading embedding model: {EMBEDDING_MODEL}")

    model = SentenceTransformer(EMBEDDING_MODEL)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
            print(f"Deleted existing collection: {COLLECTION_NAME}")
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    ids = [chunk["id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [clean_metadata(chunk["metadata"]) for chunk in chunks]

    print("Embedding chunks...")
    embeddings = model.encode(documents, show_progress_bar=True).tolist()

    print("Adding chunks to ChromaDB...")
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Vector store built.")
    print(f"Collection count: {collection.count()}")
    print(f"Saved to: {CHROMA_DIR}")

    return collection, model


def get_collection_and_model():
    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(COLLECTION_NAME)
    return collection, model


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    collection, model = get_collection_and_model()

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved = []

    for i in range(len(results["ids"][0])):
        retrieved.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })

    return retrieved


def print_results(query: str, top_k: int = TOP_K):
    print("\n" + "=" * 100)
    print(f"QUERY: {query}")
    print("=" * 100)

    results = retrieve(query, top_k=top_k)

    for rank, result in enumerate(results, start=1):
        metadata = result["metadata"]
        wrapped_text = textwrap.fill(result["text"], width=100)

        print(f"\n--- Result {rank} ---")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Source: {metadata.get('title', '')}")
        print(f"URL: {metadata.get('url', '')}")
        print(f"Chunk: {result['id']}")
        print()
        print(wrapped_text)


def run_eval_queries():
    test_queries = [
        "What makes a CS portfolio project look generic or unimpressive?",
        "How can a student make an AI-assisted project show real skill instead of looking AI-generated?",
        "Do recruiters or hiring teams actually look through GitHub projects?",
        "Should college students include class projects on a CS resume or portfolio?",
        "What should a strong project entry include on a resume, GitHub, or portfolio site?",
    ]

    for query in test_queries[:3]:
        print_results(query, top_k=TOP_K)


if __name__ == "__main__":
    build_vector_store(reset=True)
    run_eval_queries()