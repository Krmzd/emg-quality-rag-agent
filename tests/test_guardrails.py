from emg_agent.guardrails import REFUSAL, fix_refusal


def test_refusal_citations_are_removed():
    answer = "The available sources do not answer this question. [1][2][3]"
    assert fix_refusal(answer) == REFUSAL

def test_normal_answer_is_unchanged():
    answer = "Four subjects took part [3]."
    assert fix_refusal(answer) == answer


def test_partial_answer_is_kept():
    answer = "Four subjects took part [3]. The available sources do not answer this question."
    assert fix_refusal(answer) == answer