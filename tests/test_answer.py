from emg_agent.answer import format_sources


def test_sources_are_numbered_from_one():
    hits = [
        {"source_id": "cede_check_2024", "location": "p. 4", "text": "Report electrode size."},
        {"source_id": "quality_tools", "location": "Flat channel", "text": "A flat channel has no variation."},
    ]

    result = format_sources(hits)

    assert result == "[1] (cede_check_2024, p. 4) Report electrode size.\n\n[2] (quality_tools, Flat channel) A flat channel has no variation."
