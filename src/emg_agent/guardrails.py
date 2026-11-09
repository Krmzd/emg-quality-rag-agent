import re
REFUSAL = "The available sources do not answer this question."

def fix_refusal(answer):
    if answer.strip().startswith(REFUSAL):
        return REFUSAL
    return answer

def invalid_citations(answer, n_sources):
    groups = re.findall(r"\[([\d,\s]+)\]", answer)
    numbers = []
    for g in groups:
        for part in g.split(","):
            numbers.append(int(part.strip()))
    return [x for x in numbers if not 1 <= x <= n_sources]