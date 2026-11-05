import json
from emg_agent.vector_store import search

def norm(text):
    return " ".join(text.split()).lower()

with open("eval/questions.json") as f:
    questions = json.load(f)

answerable = [q for q in questions if q["answerable"]]
print(len(answerable), "answerable questions")

hits_count = 0

for q in answerable:
    results = search(q["question"], k=5)

    found = False
    for r in results:
        if norm(q["evidence"]) in norm(r["text"]):
            found = True

    if found:
        hits_count = hits_count + 1
        print("✅", q["id"], q["question"])
    else:
        print("❌", q["id"], q["question"])

print()
print(f"Hit rate: {hits_count} / {len(answerable)} = {hits_count / len(answerable):.0%}")
