from emg_agent.keyword_search import keyword_search
from emg_agent.vector_store import search

def hybrid_search(question, k=5, candidates=20):
    vector_hits = search(question, k=candidates)
    keyword_hits = keyword_search(question, k=candidates)

    rrf = {}
    by_id = {}

    for rank, hit in enumerate(vector_hits, start=1):
        cid = hit["chunk_id"]
        rrf[cid] = rrf.get(cid, 0) + 1 / (60 + rank)
        by_id[cid] = hit

    for rank, hit in enumerate(keyword_hits, start=1):
        cid = hit["chunk_id"]
        rrf[cid] = rrf.get(cid, 0) + 1 / (60 + rank)
        by_id[cid] = hit

    top_ids = sorted(rrf, key=lambda cid: rrf[cid], reverse=True)[:k]
    return [by_id[cid] for cid in top_ids]