from emg_agent.documents import clean_text, split_text


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


def test_long_text_without_full_stops_is_split():
    text = "word " * 2000

    chunks = split_text(text, max_chars=1000)

    assert all(len(chunk) <= 1000 for chunk in chunks)
