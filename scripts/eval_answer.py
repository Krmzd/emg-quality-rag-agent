import json
import re

from emg_agent.answer import answer_question

REFUSAL = "The available sources do not answer this question."

with open("eval/questions.json") as f:
    questions = json.load(f)

sample = questions
ok_count = 0
results = []

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

with open("data/eval_answers.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)