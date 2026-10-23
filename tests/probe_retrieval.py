from src.embed_index import load

vs = load()
QUESTIONS = [
    # in scope
    "What is a heap?",
    "How does build-heap work and why is it O(n)?",
    "What is the time complexity of heap sort?",
    "How do you find the parent and children of index i in the array?",
    "Is heap sort in place?",
    # out of scope
    "How does Dijkstra's algorithm work?",
    "Who won the 2018 World Cup?",
    "What is a neural network?",
]
for q in QUESTIONS:
    print("\nQ:", q)
    for doc, dist in vs.similarity_search_with_score(q, k=3):
        cos = 1 - dist ** 2 / 2
        print(f"  {cos:.3f}  [{doc.metadata['kind']} {doc.metadata['locator']}] "
              f"{doc.page_content[:70]!r}")