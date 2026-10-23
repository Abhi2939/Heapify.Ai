import json, re
from collections import Counter
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src import config as C

# Add fixes as you find them in the transcript (grep documents.jsonl for oddities)
TERM_FIXES = {
    r"\bheap if(y|i)\b": "heapify",
    r"\bheap sword\b": "heap sort",
    r"\bmax keep\b": "max heap",
}


def load_docs():
    with (C.PROCESSED / "documents.jsonl").open(encoding="utf-8") as f:
        return [Document(page_content=r["text"], metadata=r["meta"])
                for r in map(json.loads, f)]


def strip_repeated_lines(docs, thresh=0.4):
    """Drop headers/footers: lines that repeat across many pages of one source."""
    by_src = {}
    for d in docs:
        by_src.setdefault(d.metadata["source_file"], []).append(d)
    for group in by_src.values():
        if len(group) < 4:
            continue
        counts = Counter(l.strip() for d in group
                         for l in set(d.page_content.splitlines()) if l.strip())
        junk = {l for l, c in counts.items() if c / len(group) >= thresh}
        for d in group:
            d.page_content = "\n".join(
                l for l in d.page_content.splitlines() if l.strip() not in junk)
    return docs


def clean_text(t):
    t = re.sub(r"-\n(\w)", r"\1", t)          # re-join hyphenated line breaks
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    for pat, rep in TERM_FIXES.items():
        t = re.sub(pat, rep, t, flags=re.I)
    return t.strip()


def chunk():
    docs = strip_repeated_lines(load_docs())
    for d in docs:
        d.page_content = clean_text(d.page_content)
    docs = [d for d in docs if len(d.page_content) > 40]

    splitters = {
        "slides": RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100),
        "transcript": RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150),
    }
    chunks = []
    for d in docs:
        sp = splitters.get(d.metadata["kind"], splitters["transcript"])
        chunks += sp.split_documents([d])
    for i, c in enumerate(chunks):
        c.metadata["chunk_id"] = i
    return chunks


if __name__ == "__main__":
    chunks = chunk()
    out = C.ROOT / "data/chunks/chunks.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps({"text": c.page_content, "meta": c.metadata}) + "\n")
    lens = [len(c.page_content) for c in chunks]
    print(f"{len(chunks)} chunks | avg {sum(lens)//len(lens)} chars | "
          f"min {min(lens)} | max {max(lens)}")
    for c in chunks[:3]:
        print("\n---", c.metadata["kind"], c.metadata["locator"])
        print(c.page_content[:300])