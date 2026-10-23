import gradio as gr
from src.generate import answer

EXAMPLES = [
    "What is a heap?",
    "How does build-heap work and why is it O(n)?",
    "Walk me through the heap sort algorithm.",
    "Is heap sort in place?",
    "What operations does a priority queue support?",
]


def fmt_sources(sources):
    lines = []
    for s in sources:
        name = f"[{s['label']}]({s['url']})" if s["url"] else s["label"]
        lines.append(f"- **[{s['n']}]** {name} (similarity {s['score']})")
    return "\n".join(lines)


def respond(message, history):
    try:
        r = answer(message)
    except Exception as e:  # rate limits, network, missing key
        return f"Something went wrong while answering ({type(e).__name__}). Please try again."
    out = r["answer"]
    if r["sources"]:
        out += "\n\n---\n**Sources**\n" + fmt_sources(r["sources"])
    return out


demo = gr.ChatInterface(
    fn=respond,
    title="Heapify.Ai: Heap Sort Tutor",
    description=(
        "Ask about heaps, priority queues, heapify, build-heap and heap sort. "
        "Answers come only from MIT 6.006 (Fall 2011) Lecture 4 (slides and "
        "transcript, MIT OpenCourseWare, CC BY-NC-SA) plus a short study-notes "
        "summary, and every answer cites its sources."
    ),
    examples=EXAMPLES,
)

if __name__ == "__main__":
    demo.launch()