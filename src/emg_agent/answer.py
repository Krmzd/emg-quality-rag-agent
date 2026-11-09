from emg_agent.hybrid import hybrid_search
from emg_agent.llm import CHAT_DEPLOYMENT, get_client
from emg_agent.guardrails import fix_refusal, REFUSAL


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
    hits = hybrid_search(question, k=k)                
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
    answer = fix_refusal(answer)

    return {"answer": answer, "sources": hits}     