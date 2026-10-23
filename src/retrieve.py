def retrieve(vs, question, k=4, threshold=0.45):
    hits = vs.similarity_search_with_score(question, k=k)   # L2 distance
    out = []
    for doc, dist in hits:
        cos = 1 - (dist ** 2) / 2        # valid for unit-length vectors
        if cos >= threshold:
            out.append((doc, cos))
    return out