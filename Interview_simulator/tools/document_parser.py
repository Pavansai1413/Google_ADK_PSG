import os
from pathlib import Path
import fitz
from docx import Document

def parse_document(file_path: Path) -> str:
    """ Extract clean text from a document (PDF or Word).
    
    Args:
        file_path (Path): Path to the document file.
    
    Returns:
        str: Extracted plain text content of the document.
    Raises:
        ValueError: If the file not found or unsupported file format.
    """

    path = Path(file_path)
    if not path.exists():
        raise ValueError(f"File not found: {file_path}")
    
    ext = path.suffix.lower()

    if ext == ".pdf":
        return parse_pdf(path)
    elif ext == ".doc" or ext == ".docx":
        return parse_docx(path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def parse_pdf(pdf_path: Path) -> str:
    text = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            page_text = page.get_text("text")
            if page_text.strip():
                text.append(page_text)
    return "\n\n".join(text).strip()

def parse_docx(docx_path: Path) -> str:
    doc = Document(docx_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs).strip()