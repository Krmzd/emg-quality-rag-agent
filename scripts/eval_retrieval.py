import sys
import json
from emg_agent.vector_store import search

def norm(text):
    return " ".join(text.split()).lower()

with open("eval/questions.json") as f:
    questions = json.load(f)

experiment = sys.argv[1]
print("Experiment:", experiment)

missed = []

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
        missed.append(q["id"])

print()
print(f"Hit rate: {hits_count} / {len(answerable)} = {hits_count / len(answerable):.0%}")
print("Missed:", missed)

summary = {
    "experiment": experiment,
    "hits": hits_count,
    "total": len(answerable),
    "hit_rate": round(hits_count / len(answerable), 2),
    "missed": missed,
}

with open(f"eval/results/{experiment}_retrieval.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Saved to", f"eval/results/{experiment}_retrieval.json")