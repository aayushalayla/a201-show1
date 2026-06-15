import os
from dotenv import load_dotenv
from groq import Groq

from src.retrieve import retrieve


MODEL_NAME = "llama-3.3-70b-versatile"
TOP_K = 5
MAX_DISTANCE = 0.65


def format_context(retrieved_chunks: list[dict]) -> tuple[str, list[str]]:
    """
    Format retrieved chunks for the LLM and create a source list.
    Sources are also returned separately so attribution is not left only to the LLM.
    """
    context_parts = []
    sources = []
    seen_sources = set()

    for i, chunk in enumerate(retrieved_chunks, start=1):
        metadata = chunk["metadata"]
        source_label = f"S{i}"

        title = metadata.get("title", "Unknown source")
        url = metadata.get("url", "")
        chunk_index = metadata.get("chunk_index", "")

        context_parts.append(
            f"[{source_label}]\n"
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Chunk index: {chunk_index}\n"
            f"Text:\n{chunk['text']}"
        )

        source_key = (title, url)

        if source_key not in seen_sources:
            source_line = f"{title}"
            if url:
                source_line += f" — {url}"
            sources.append(source_line)
            seen_sources.add(source_key)

    return "\n\n---\n\n".join(context_parts), sources


def build_messages(question: str, context: str) -> list[dict]:
    system_prompt = """
You are a grounded question-answering assistant for an unofficial guide to CS portfolio side projects.

You must follow these rules:
1. Answer using only the provided retrieved context.
2. Do not use outside knowledge, even if you know the answer.
3. If the retrieved context does not contain enough information, say: "I don't have enough information in the retrieved documents to answer that."
4. Cite the context chunks you use with bracketed source labels like [S1] or [S2].
5. Do not invent sources, URLs, statistics, recruiter behavior, or advice not supported by the context.
6. Be concise but specific.
""".strip()

    user_prompt = f"""
Retrieved context:

{context}

Question:
{question}

Answer the question using only the retrieved context. Include bracketed source citations like [S1].
""".strip()

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def ask(question: str) -> dict:
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY. Add it to your .env file.")

    if not question.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "retrieved_chunks": [],
        }

    retrieved_chunks = retrieve(question, top_k=TOP_K)

    if not retrieved_chunks:
        return {
            "answer": "I don't have enough information in the retrieved documents to answer that.",
            "sources": [],
            "retrieved_chunks": [],
        }

    best_distance = retrieved_chunks[0]["distance"]

    if best_distance > MAX_DISTANCE:
        return {
            "answer": "I don't have enough information in the retrieved documents to answer that.",
            "sources": [],
            "retrieved_chunks": retrieved_chunks,
        }

    context, sources = format_context(retrieved_chunks)
    messages = build_messages(question, context)

    client = Groq(api_key=api_key)

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
        max_tokens=700,
    )

    answer = completion.choices[0].message.content.strip()

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks,
    }


if __name__ == "__main__":
    test_question = "Do recruiters or hiring teams actually look through GitHub projects?"
    result = ask(test_question)

    print("\nANSWER:\n")
    print(result["answer"])

    print("\nSOURCES:\n")
    for source in result["sources"]:
        print(f"- {source}")