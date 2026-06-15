import gradio as gr

from src.query import ask


def handle_query(question: str):
    try:
        result = ask(question)

        answer = result["answer"]

        sources = "\n".join(f"• {source}" for source in result["sources"])
        if not sources:
            sources = "No sources returned."

        retrieved = []

        for i, chunk in enumerate(result["retrieved_chunks"], start=1):
            metadata = chunk["metadata"]
            title = metadata.get("title", "Unknown source")
            url = metadata.get("url", "")
            distance = chunk.get("distance", "")

            preview = chunk["text"][:700].replace("\n", " ")

            retrieved.append(
                f"Result {i}\n"
                f"Distance: {distance:.4f}\n"
                f"Source: {title}\n"
                f"URL: {url}\n"
                f"Preview: {preview}"
            )

        retrieved_text = "\n\n---\n\n".join(retrieved)

        return answer, sources, retrieved_text

    except Exception as e:
        return f"Error: {e}", "", ""


with gr.Blocks(title="The Unofficial Guide to CS Portfolio Projects") as demo:
    gr.Markdown("# The Unofficial Guide to CS Portfolio Projects")
    gr.Markdown(
        "Ask a question about CS side projects, GitHub portfolios, class projects, AI-assisted projects, or recruiter behavior."
    )

    question = gr.Textbox(
        label="Your question",
        placeholder="Example: Do recruiters actually look through GitHub projects?",
        lines=2,
    )

    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=6)
    retrieved_chunks = gr.Textbox(label="Retrieved chunks", lines=14)

    ask_button.click(
        handle_query,
        inputs=question,
        outputs=[answer, sources, retrieved_chunks],
    )

    question.submit(
        handle_query,
        inputs=question,
        outputs=[answer, sources, retrieved_chunks],
    )


if __name__ == "__main__":
    demo.launch()