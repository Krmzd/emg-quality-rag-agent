import chromadb

from emg_agent.documents import load_documents, make_chunks
from emg_agent.llm import embed_texts

CHROMA_PATH = "data/chroma"
COLLECTION_NAME = "emg_docs"


def build_index():
    """
    Load all documents, cut them into chunks, embed the chunks,
    and store them in Chroma. Any old index is replaced.

    Returns:
        The number of chunks stored.
    """
    chunks = make_chunks(load_documents())
    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(COLLECTION_NAME)

    collection.add(
        ids=[c["chunk_id"] for c in chunks],
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"source_id": c["source_id"], "location": c["location"]} for c in chunks],
    )
    return len(chunks)
