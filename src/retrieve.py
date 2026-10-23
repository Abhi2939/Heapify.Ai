def _words(t):
    return set(t.lower().split())


def retrieve(vs, question, k=4, floor=0.65, fetch=12, dup=0.8):
    """Return up to k (Document, cosine) pairs, best first, near-duplicates removed."""
    hits = vs.similarity_search_with_score(question, k=fetch)  # score = cosine
    picked = []
    for doc, cos in hits:
        cos = float(cos)
        if cos < floor:
            break
        w = _words(doc.page_content)
        if any(len(w & pw) / max(len(w | pw), 1) > dup for _, _, pw in picked):
            continue
        picked.append((doc, cos, w))
        if len(picked) == k:
            break
    return [(d, c) for d, c, _ in picked]


if __name__ == "__main__":
    from src.embed_index import load
    vs = load()
    for q in ["What is the time complexity of heap sort?", "Who won the 2018 World Cup?"]:
        res = retrieve(vs, q)
        print(f"\nQ: {q}  ->  {len(res)} chunks above floor")
        for d, c in res:
            print(f"  {c:.3f} [{d.metadata['kind']} {d.metadata['locator']}] "
                  f"{d.page_content[:70]!r}")