from emg_agent.vector_store import build_index

count = build_index()
print(f"Stored {count} chunks in Chroma.")
