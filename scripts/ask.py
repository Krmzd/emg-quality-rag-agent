import sys
from emg_agent.answer import answer_question

question = sys.argv[1]

result = answer_question(question)

print (result['answer'])
if result["invalid_citations"]:
    print("Warning: these citations do not match any source:", result["invalid_citations"])
print()
print("sources:")
for number, hit in enumerate(result["sources"], start = 1):
	print(f"[{number}] {hit['source_id']}, {hit['location']}")
