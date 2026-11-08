import re
from rank_bm25 import BM25Okapi
from emg_agent.documents import load_documents, make_chunks

def tokenize(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return words

def keyword_search(question, k=5):
    chunks = make_chunks(load_documents())
    tokenized = [tokenize(c["text"]) for c in chunks]
    bm25 = BM25Okapi(tokenized)
    scores = bm25.get_scores(tokenize(question))
    order = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)

    results = []
    for i in order[:k]:
         results.append(
            {
                "chunk_id": chunks[i]["chunk_id"],
                "source_id": chunks[i]["source_id"],
                "location": chunks[i]["location"],
                "text": chunks[i]["text"],
                "score": scores[i],
            }
        )
    return results
