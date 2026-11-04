from emg_agent.vector_store import search
def format_sources(hits):
	"""
	Put the retrieved chunks into one text, numbered [1], [2], ...
	so the LLM can cite them by number.
	"""
	parts = []
	for number, hit in enumerate(hits, start=1):
		parts.append(f"[{number}] ({hit['source_id']}, {hit['location']}) {hit['text']}")
	return "\n\n".join(parts) 
