"""
app.py — Gradio interface for the UB CS Unofficial Guide RAG app.

Run:
    python app.py
"""

import gradio as gr
from query import ask


def handle_query(question):
    result = ask(question)
    sources = "\n".join(
        f"• {s['source_file']}  (chunk {s['chunk_index']})"
        for s in result["sources"]
    )
    return result["answer"], sources


with gr.Blocks(title="UB CS Unofficial Guide") as demo:
    gr.Markdown("## UB CS Unofficial Guide")
    gr.Markdown("Ask questions about studying CS at UB. Answers are grounded in real student advice.")

    inp = gr.Textbox(label="Your question", placeholder="e.g. What do students say about CSE 250?")
    btn = gr.Button("Ask")
    answer  = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


demo.launch()
