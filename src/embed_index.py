import json
import numpy as np
from fastembed import TextEmbedding
from langchain_core.documents import Document
from src import config as C

MODEL = "BAAI/bge-small-en-v1.5"
INDEX = C.ROOT / "index"
_model = None


def embed(texts):
    """Unit-length vectors, so a dot product is the cosine similarity."""
    global _model
    if _model is None:
        _model = TextEmbedding(MODEL)
    v = np.array(list(_model.embed(texts)), dtype="float32")
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def build():
    from src.chunk import chunk          # build-time only
    chunks = chunk()
    vecs = embed([c.page_content for c in chunks])
    INDEX.mkdir(exist_ok=True)
    np.save(INDEX / "vectors.npy", vecs)
    items = [{"text": c.page_content, "meta": c.metadata} for c in chunks]
    (INDEX / "chunks.json").write_text(
        json.dumps(items, default=str), encoding="utf-8")
    print(f"Indexed {len(chunks)} chunks -> {INDEX}")


def load():
    vecs = np.load(INDEX / "vectors.npy")
    items = json.loads((INDEX / "chunks.json").read_text(encoding="utf-8"))
    docs = [Document(page_content=i["text"], metadata=i["meta"]) for i in items]
    return vecs, docs


if __name__ == "__main__":
    build()