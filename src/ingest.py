import json
import re
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from src import config as C

TS = re.compile(
    r"(?:(\d+):)?(\d{1,2}):(\d{2})[.,](\d{3})\s*-->\s*(?:\d+:)?\d{1,2}:\d{2}[.,]\d{3}"
)


def fmt(t):
    t = int(t)
    return f"{t // 60:02d}:{t % 60:02d}"


def base_meta(kind, source_file):
    return dict(course=C.COURSE, lecture=C.LECTURE, url=C.LECTURE_URL,
                kind=kind, source_file=source_file)


def load_pdf(path, kind):
    docs = PyPDFLoader(str(path)).load()
    for d in docs:
        d.metadata = {**base_meta(kind, path.name),
                      "locator": f"p.{d.metadata.get('page', 0) + 1}"}
    return docs


def parse_timed(text):
    """Parse .vtt/.srt into [(start_seconds, text)] cues."""
    cues, start, buf = [], None, []
    for line in text.splitlines():
        m = TS.search(line)
        if m:
            if start is not None and buf:
                cues.append((start, " ".join(buf)))
            h, mi, s = int(m.group(1) or 0), int(m.group(2)), int(m.group(3))
            start, buf = h * 3600 + mi * 60 + s, []
        elif line.strip() and not line.strip().isdigit() \
                and not line.startswith(("WEBVTT", "NOTE", "Kind:", "Language:")):
            buf.append(re.sub(r"<[^>]+>", "", line.strip()))
    if start is not None and buf:
        cues.append((start, " ".join(buf)))
    return cues


def load_timed(path):
    cues = parse_timed(path.read_text(encoding="utf-8", errors="ignore"))
    docs, buf, t0 = [], [], None
    for start, txt in cues:
        if t0 is None:
            t0 = start
        buf.append(txt)
        if start - t0 >= C.WINDOW_SEC:
            docs.append(timed_doc(path, buf, t0))
            buf, t0 = [], None
    if buf:
        docs.append(timed_doc(path, buf, t0))
    return docs


def timed_doc(path, buf, t0):
    meta = {**base_meta("transcript", path.name), "locator": fmt(t0)}
    return Document(page_content=" ".join(buf), metadata=meta)


def load_plain(path):
    docs = TextLoader(str(path), encoding="utf-8", autodetect_encoding=True).load()
    for d in docs:
        d.metadata = {**base_meta("transcript", path.name), "locator": "transcript"}
    return docs


def ingest():
    docs = []
    for p in sorted(C.RAW_NOTES.glob("*.pdf")):
        docs += load_pdf(p, "slides")
    for p in sorted(C.RAW_TRANSCRIPTS.iterdir()):
        ext = p.suffix.lower()
        if ext in {".vtt", ".srt"}:
            docs += load_timed(p)
        elif ext == ".txt":
            docs += load_plain(p)
        elif ext == ".pdf":
            docs += load_pdf(p, "transcript")
    return docs


if __name__ == "__main__":
    docs = ingest()
    C.PROCESSED.mkdir(parents=True, exist_ok=True)
    out = C.PROCESSED / "documents.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps({"text": d.page_content, "meta": d.metadata}) + "\n")

    by = {}
    for d in docs:
        k = (d.metadata["kind"], d.metadata["source_file"])
        n, c = by.get(k, (0, 0))
        by[k] = (n + 1, c + len(d.page_content))
    for (kind, name), (n, c) in by.items():
        print(f"{kind:10} {name}: {n} docs, {c} chars")
    print(f"\nTotal {len(docs)} docs -> {out}")
    for d in docs[:2] + docs[-2:]:
        print("\n---", d.metadata["kind"], d.metadata["locator"])
        print(d.page_content[:300])