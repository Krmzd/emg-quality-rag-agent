from emg_agent.vector_store import search
from emg_agent.llm import CHAT_DEPLOYMENT, get_client

SYSTEM_PROMPT = """You are an assistant for EMG researchers.

1. Answer only using the numbered sources provided below the question.
2. After each statement, cite the source number in brackets, like [1] or [2].
3. If the sources do not contain the answer, say exactly:
   "The available sources do not answer this question."
4. Never make up information. Do not state numbers, thresholds or measurements
   that are not in the sources. Do not diagnose patients or give medical advice.
5. Keep answers short and clear. Technical EMG terms are fine.
"""

def format_sources(hits):
	"""
	Put the retrieved chunks into one text, numbered [1], [2], ...
	so the LLM can cite them by number.
	"""
	parts = []
	for number, hit in enumerate(hits, start=1):
		parts.append(f"[{number}] ({hit['source_id']}, {hit['location']}) {hit['text']}")
	return "\n\n".join(parts) 

def answer_question(question, k=5):
    """
    Answer a question using the k most relevant chunks, with citations.

    Returns:
        A dictionary with:
            answer: the text written by the model, with [1], [2] citations.
            sources: the hits that were numbered [1], [2], ...
    """
    hits = search(question, k=k)                
    sources_text = format_sources(hits)          

    client = get_client()
    response = client.chat.completions.create(      
        model=CHAT_DEPLOYMENT,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Sources:\n\n{sources_text}\n\nQuestion: {question}"},
        ],
        max_completion_tokens=2000
    )
    answer = response.choices[0].message.content

    return {"answer": answer, "sources": hits}     