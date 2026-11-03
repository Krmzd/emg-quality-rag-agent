import sys

from emg_agent.vector_store import search

question = sys.argv[1]

for hit in search(question):
    print(f"{hit['distance']:.3f}  {hit['source_id']} | {hit['location']}")
    print("   ", hit["text"][:150])
    print()
