import json
import sys

from emg_agent.agent import build_agent

experiment = sys.argv[1]

with open("eval/agent_questions.json") as f:
    questions = json.load(f)

agent = build_agent()
ok_count = 0
failed = []

for q in questions:
    config = {"configurable": {"thread_id": q["id"]}}
    blocked = False
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": q["question"]}]}, config)
    except Exception as e:
        if "content management policy" not in str(e):
            raise
        blocked = True

    tools_used = []
    if not blocked:
        for m in result["messages"]:
            for call in getattr(m, "tool_calls", []):
                tools_used.append(call["name"])

    used = tools_used[0] if tools_used else None
    ok = used == q["expected_tool"]

    print("✅" if ok else "❌", q["id"], q["question"])
    print("   expected:", q["expected_tool"], "| used:", tools_used)
 
    if ok:
        ok_count = ok_count + 1
    else:
        failed.append(q["id"])

print(f"Passed: {ok_count} / {len(questions)}")

summary = {
    "experiment": experiment,
    "passed": ok_count,
    "total": len(questions),
    "failed": failed,
}

with open(f"eval/results/{experiment}_agent.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Saved to", f"eval/results/{experiment}_agent.json")