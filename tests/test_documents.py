from emg_agent.documents import clean_text


def test_hyphenated_word_is_joined():
    text = "resubmit-\nted"

    result = clean_text(text)

    assert result == "resubmitted"

def test_line_break_becomes_space():
	text = "project: \nChecklist"
	
	result = clean_text(text)

	assert result == "project: Checklist"

def test_repeated_spaces_are_collapsed():
	text = "two  spaces"

	result = clean_text(text)

	assert result == "two spaces"
