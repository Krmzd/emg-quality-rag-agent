import sys
import json
import re

from emg_agent.answer import answer_question

REFUSAL = "The available sources do not answer this question."

with open("eval/questions.json") as f:
    questions = json.load(f)

experiment = sys.argv[1]
print("Experiment:", experiment)

sample = questions
ok_count = 0
results = []
failed = []
bad_citations = []

for q in sample:
    result = answer_question(q["question"])
    answer = result["answer"]

    refused = REFUSAL in answer
    groups = re.findall(r"\[([\d,\s]+)\]", answer)
    numbers = []
    for g in groups:
        for part in g.split(","):
            numbers.append(part.strip())
    cited = len(numbers) > 0

    n_sources = len(result["sources"])
    valid_citations = all(1 <= int(x) <= n_sources for x in numbers)

    if q["answerable"]:
        ok = cited and not refused
    else:
        ok = refused
    if not ok:
        failed.append(q["id"])
    if not valid_citations:
        bad_citations.append(q["id"])

    print("✅" if ok else "❌", q["id"], q["question"])
    print("   refused:", refused, "| cited:", cited, "| valid citations:", valid_citations)
    print("   EXPECTED:", q["answer"])
    print("   ANSWER:  ", answer)
    print()
    if ok:
        ok_count = ok_count + 1
    results.append({"id": q["id"], "question": q["question"], "expected": q["answer"],
                    "answer": answer, "refused": refused, "cited": cited, "ok": ok})

print(f"Passed: {ok_count} / {len(sample)}")

with open(f"data/{experiment}_answer.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

summary = {
    "experiment": experiment,
    "passed": ok_count,
    "total": len(results),
    "failed": failed,
    "bad_citations": bad_citations,
}

with open(f"eval/results/{experiment}_answers.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Saved to", f"eval/results/{experiment}_answers.json")