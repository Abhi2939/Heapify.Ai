import numpy as np
from src.embed_index import embed


def search(store, question, k):
    vecs, docs = store
    scores = vecs @ embed([question])[0]
    order = np.argsort(-scores)[:k]
    return [(docs[i], float(scores[i])) for i in order]


def _words(t):
    return set(t.lower().split())


def retrieve(store, question, k=4, floor=0.65, fetch=12, dup=0.8):
    picked = []
    for doc, cos in search(store, question, fetch):   # best first
        if cos < floor:
            break
        w = _words(doc.page_content)
        if any(len(w & pw) / max(len(w | pw), 1) > dup for _, _, pw in picked):
            continue
        picked.append((doc, cos, w))
        if len(picked) == k:
            break
    return [(d, c) for d, c, _ in picked]