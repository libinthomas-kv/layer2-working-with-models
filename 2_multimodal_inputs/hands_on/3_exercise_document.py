"""
Hands-on 3 (Multimodal): Document understanding — text, PDF, image.

(a) Extract from raw text: role in system, context + query in user.
(b) Extract from PDF: read PDF to text (pypdf), then same as (a).
Run from repo root:  python 2_multimodal_inputs/hands_on/3_exercise_document.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from client import complete

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

# TODO 3.1: System prompt: role (document extraction assistant) + rule (extract only from context, output format).
DOC_SYSTEM = "" # <-- fill in

def exercise_3_extract(doc_text: str, query: str) -> str:
    """Extract information from doc_text according to query."""
    user = f"## Context\n{doc_text}\n\n## Query\n{query}"
    return complete(DOC_SYSTEM, user)


def pdf_to_text(pdf_path: str | Path) -> str:
    """Extract text from PDF. Requires pypdf. Returns error string if missing or file not found."""
    if PdfReader is None:
        return "[Install pypdf: pip install pypdf]"
    path = Path(pdf_path)
    if not path.exists():
        return f"[File not found: {path}]"
    reader = PdfReader(path)
    parts = [p.extract_text() or "" for p in reader.pages]
    return "\n\n".join(parts).strip()


def exercise_3_extract_from_pdf(pdf_path: str | Path, query: str) -> str:
    """Read PDF to text, then extract using DOC_SYSTEM and exercise_3_extract."""
    doc_text = pdf_to_text(pdf_path)
    return exercise_3_extract(doc_text, query)


if __name__ == "__main__":
    sample = "Acme Corp and Beta Inc signed a deal on 2024-01-15. Total value: $2.5M. Contact: Jane Doe."
    print("From text — summary:", exercise_3_extract(sample, "Give a one-line summary."))
    print("From text — entities:", exercise_3_extract(sample, "List company names, date, amount, and contact name."))
    # PDF in hands_on folder (same dir as this script)
    pdf_path = Path(__file__).resolve().parent / "AI.pdf"
    if pdf_path.exists():
        print("From PDF:", exercise_3_extract_from_pdf(pdf_path, "List the main headings or topics."))
    else:
        print("(Add 2_multimodal_inputs/hands_on/AI.pdf to try extract_from_pdf.)")
