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


def search(question, k=5):
    """
    Find the k chunks most similar in meaning to the question.

    Returns:
        A list of dictionaries (closest first), each with:
            chunk_id, source_id, location, text, and distance
            (smaller distance = more similar).
    """
    query_vector = embed_texts([question])[0]

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(COLLECTION_NAME)
    results = collection.query(query_embeddings=[query_vector], n_results=k)

    hits = []
    for i in range(len(results["ids"][0])):
        hits.append(
            {
                "chunk_id": results["ids"][0][i],
                "source_id": results["metadatas"][0][i]["source_id"],
                "location": results["metadatas"][0][i]["location"],
                "text": results["documents"][0][i],
                "distance": results["distances"][0][i],
            }
        )
    return hits