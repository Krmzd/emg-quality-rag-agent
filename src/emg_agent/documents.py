import re


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
