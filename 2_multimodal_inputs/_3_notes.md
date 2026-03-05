# Session 3: Document understanding — PDFs, tables, unstructured content

- **OCR** fits here as part of the pipeline, not as a standalone topic: document → (extract text or render pages as images) → LLM.
- Two common paths:
  - **Text path**: PDF/text extraction (e.g. pypdf, pdfplumber) → raw text → LLM with instruction/context/query.
  - **Vision path**: Render page as image (or scan) → vision model with "extract X" prompt.
- Use same structure: role (e.g. "document extraction assistant"), context (document text or image), query (what to extract, format).
- Tables: extract as text or pass table image to vision model; ask for structured output (e.g. JSON).
