import json
import re
from pypdf import PdfReader

def clean_text(text):
    """
    Clean text extracted from a PDF.

    Joins words split across lines with a hyphen, replaces line breaks
    with spaces, and collapses repeated spaces.

    Parameters:
        text: raw text from a PDF page.

    Returns:
        The cleaned text as one string.
    """
    text = re.sub(r"-\n(\w)", r"\1", text)
    text = re.sub(r"\s*\n\s*", " ", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()

def load_pdf(path):
    """
    Read a PDF and return the cleaned text of each page.

    Parameters:
        path: path to the PDF file.

    Returns:
        A list with one dictionary per page:
            page: page number, starting at 1.
            text: the cleaned text of that page.
    """
    reader = PdfReader(path)

    pages = []
    for i, page in enumerate(reader.pages):
        text = clean_text(page.extract_text())
        if text:
            pages.append({"page": i + 1, "text": text})

    return pages


def load_markdown(path):
    """
    Read a Markdown file and split it into sections at each "## " heading.

    Parameters:
        path: path to the .md file.

    Returns:
        A list with one dictionary per section:
            section: the heading text.
            text: the text under that heading.
    """
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    sections = []
    heading = "Introduction"
    current = []

    for line in lines:
        if line.startswith("## "):
            if current:
                sections.append({"section": heading, "text": "\n".join(current).strip()})
            heading = line[3:].strip()
            current = []
        elif line.startswith("# "):
            continue
        else:
            current.append(line)

    if current:
        sections.append({"section": heading, "text": "\n".join(current).strip()})

    return [s for s in sections if s["text"]]


def load_text(path):
    """
    Read a plain-text file as one piece.

    Returns:
        A list with one dictionary: section "full text" and the file's text.
    """
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read().strip()
    return [{"section": "full text", "text": text}]

def load_documents(sources_path="docs/sources.json"):
    """
    Load every document listed in sources.json.

    Returns:
        A list of dictionaries, each with:
            source_id: the document's id from sources.json.
            location: page (e.g. "p. 3") or section name.
            text: the text of that page or section.
    """
    with open(sources_path, encoding="utf-8") as f:
        sources = json.load(f)

    passages = []
    for source in sources:
        path = source["file"]

        if path.endswith(".pdf"):
            for p in load_pdf(path):
                passages.append({"source_id": source["id"], "location": f"p. {p['page']}", "text": p["text"]})
        elif path.endswith(".md"):
            for s in load_markdown(path):
                passages.append({"source_id": source["id"], "location": s["section"], "text": s["text"]})
        else:
            for s in load_text(path):
                passages.append({"source_id": source["id"], "location": s["section"], "text": s["text"]})

    return passages