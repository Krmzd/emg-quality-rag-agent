from emg_agent.guardrails import REFUSAL, fix_refusal, invalid_citations


def test_refusal_citations_are_removed():
    answer = "The available sources do not answer this question. [1][2][3]"
    assert fix_refusal(answer) == REFUSAL

def test_normal_answer_is_unchanged():
    answer = "Four subjects took part [3]."
    assert fix_refusal(answer) == answer


def test_partial_answer_is_kept():
    answer = "Four subjects took part [3]. The available sources do not answer this question."
    assert fix_refusal(answer) == answer

def test_invented_citation_is_found():
    answer = "Report the distance [2]. Use a filter [8]."
    assert invalid_citations(answer, n_sources=5) == [8]


def test_valid_citations_return_empty():
    answer = "Report the distance [1, 2]."
    assert invalid_citations(answer, n_sources=5) == []