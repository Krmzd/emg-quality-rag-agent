REFUSAL = "The available sources do not answer this question."

def fix_refusal(answer):
    if answer.strip().startswith(REFUSAL):
        return REFUSAL
    return answer