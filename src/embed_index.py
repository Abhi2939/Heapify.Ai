from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_huggingface import HuggingFaceEmbeddings
from src import config as C
from src.chunk import chunk

EMBED_MODEL = "BAAI/bge-small-en-v1.5"
INDEX_DIR = C.ROOT / "index"
STRATEGY = DistanceStrategy.MAX_INNER_PRODUCT


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        encode_kwargs={"normalize_embeddings": True},  # needed for cosine math below
    )


def build():
    chunks = chunk()
    vs = FAISS.from_documents(chunks, get_embeddings(),distance_strategy=STRATEGY)
    INDEX_DIR.mkdir(exist_ok=True)
    vs.save_local(str(INDEX_DIR))
    print(f"Indexed {len(chunks)} chunks -> {INDEX_DIR}")


def load():
    return FAISS.load_local(
        str(INDEX_DIR), get_embeddings(),
        allow_dangerous_deserialization=True,  # our own index file
        distance_strategy=STRATEGY,
    )

if __name__ == "__main__":
    build()