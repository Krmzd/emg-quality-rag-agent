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


def split_sentences(text):
    """
    Split text into sentences at ".", "!" or "?" followed by a space.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s for s in sentences if s]

def split_long_sentence(sentence, max_chars):
    """
    Split a sentence longer than max_chars into pieces of whole words.
    A sentence that is short enough is returned unchanged, in a list.
    """
    if len(sentence) <= max_chars:
        return [sentence]

    pieces = []
    current = ""
    for word in sentence.split():
        if current and len(current) + 1 + len(word) > max_chars:
            pieces.append(current)
            current = word
        else:
            current = f"{current} {word}" if current else word

    if current:
        pieces.append(current)

    return pieces


def split_text(text, max_chars=1000, overlap_sentences=1):
    """
    Group sentences into chunks of at most max_chars characters.

    Parameters:
        text: the text to split.
        max_chars: maximum chunk length in characters. Default 1000.
            A single sentence longer than this becomes its own chunk.
        overlap_sentences: how many sentences from the end of one chunk
            are repeated at the start of the next. Default 1.

    Returns:
        A list of chunk texts.
    """
    sentences = []
    for s in split_sentences(text):
        sentences.extend(split_long_sentence(s, max_chars))

    chunks = []
    current = []

    for sentence in sentences:
        if current and len(" ".join(current + [sentence])) > max_chars:
            chunks.append(" ".join(current))
            current = current[-overlap_sentences:] if overlap_sentences else []
            if len(" ".join(current + [sentence])) > max_chars:
                current = []
        current.append(sentence)

    if current:
        chunks.append(" ".join(current))

    return chunks


def make_chunks(passages, max_chars=1000, overlap_sentences=1):
    """
    Split every passage into chunks, keeping its source and location.

    Returns:
        A list of dictionaries, each with:
            chunk_id: a unique id, e.g. "cede_check_2024:p. 3:0".
            source_id, location: copied from the passage.
            text: the chunk text.
    """
    chunks = []
    for p in passages:
        for i, text in enumerate(split_text(p["text"], max_chars, overlap_sentences)):
            chunks.append(
                {
                    "chunk_id": f"{p['source_id']}:{p['location']}:{i}",
                    "source_id": p["source_id"],
                    "location": p["location"],
                    "text": text,
                }
            )
    return chunks