from src.embed_index import load

vs = load()
QUESTIONS = [
    # in scope
    "What is a heap?",
    "How does build-heap work and why is it O(n)?",
    "What is the time complexity of heap sort?",
    "How do you find the parent and children of index i in the array?",
    "Is heap sort in place?",
    "What operations does a priority queue support?",
    # near-miss / out of scope
    "How does Dijkstra's algorithm work?",
    "How does quicksort work?",
    "What is a binary search tree?",
    "Explain merge sort",
    "How do I implement a priority queue in Python?",
    "What is a neural network?",
    "Who won the 2018 World Cup?",
]
for q in QUESTIONS:
    print("\nQ:", q)
    for doc, score in vs.similarity_search_with_score(q, k=3):
        print(f"  {float(score):.3f}  [{doc.metadata['kind']} {doc.metadata['locator']}] "
              f"{doc.page_content[:70]!r}")