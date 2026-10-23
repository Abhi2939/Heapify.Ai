from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_NOTES = ROOT / "data/raw/notes"
RAW_TRANSCRIPTS = ROOT / "data/raw/transcripts"
PROCESSED = ROOT / "data/processed"

COURSE = "MIT 6.006 Fall 2011"
LECTURE = "Lecture 4: Heaps and Heap Sort"
STUDY_NOTES = ROOT / "data/study_notes"

LECTURE_URL = (
    "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/"
    "6-006-introduction-to-algorithms-fall-2011/lecture-videos/"
    "lecture-4-heaps-and-heap-sort/"
)
WINDOW_SEC = 45  