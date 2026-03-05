"""
Session 3 (Multimodal): Document understanding — PDFs, tables, unstructured content.

- Raw text: extract_from_text(doc_text, query)
- PDF file: extract_from_pdf(pdf_path, query) — uses pypdf to get text, then LLM
- Image: extract_from_image(image_url, query) — vision model

OCR fits in this pipeline: scan -> image -> vision or OCR lib -> text -> LLM.

Run from repo root:  python 2_multimodal_inputs/3_document_understanding.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from client import complete, complete_vision

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


# Text-based: when you already have extracted text (e.g. from pypdf, pdfplumber)
SYSTEM_DOC_EXTRACT = (
    "You are a document extraction assistant. "
    "Extract only what is asked from the provided text. "
    "Output in the requested format (e.g. JSON, list). Do not invent information."
)


def extract_from_text(doc_text: str, query: str) -> str:
    """Extract information from already-extracted document text."""
    user = f"## Context\n{doc_text}\n\n## Query\n{query}"
    return complete(SYSTEM_DOC_EXTRACT, user)


def pdf_to_text(pdf_path: str | Path) -> str:
    """Extract text from a PDF file. Requires pypdf. Returns concatenated text of all pages."""
    if PdfReader is None:
        return "[Install pypdf to read PDFs: pip install pypdf]"
    path = Path(pdf_path)
    if not path.exists():
        return f"[File not found: {path}]"
    reader = PdfReader(path)
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n\n".join(parts).strip()


def extract_from_pdf(pdf_path: str | Path, query: str) -> str:
    """Read PDF, extract text with pypdf, then run extraction query via LLM."""
    doc_text = pdf_to_text(pdf_path)
    if doc_text.startswith("["):
        return doc_text  # error message
    return extract_from_text(doc_text, query)


# Vision-based: when document is an image (e.g. scanned page, screenshot)
def extract_from_image(image_url: str, query: str) -> str:
    """Extract information from a document image (vision model)."""
    return complete_vision(SYSTEM_DOC_EXTRACT, query, image_url)


def run_demo():
    pdf_path = Path(__file__).resolve().parent / "Multimodal Inputs.pdf"
    print("extract_from_text: ", extract_from_text("Acme Corp and Beta Inc signed a deal on 2024-01-15. Total value: $2.5M. Contact: Jane Doe.", "Give a one-line summary."))
    print("extract_from_pdf: ", extract_from_pdf(pdf_path, "List the main headings or topics."))
    print("extract_from_image: ", extract_from_image("https://miro.medium.com/v2/resize:fit:720/format:webp/1*xfboC-sVIT2hzWkgQZT_7w.png", "What is in this image?"))

if __name__ == "__main__":
    run_demo()
