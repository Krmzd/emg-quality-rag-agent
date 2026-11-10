from langchain_core.tools import tool

from emg_agent.answer import answer_question
from emg_agent.data import FS, LINE_FREQ, load_recording
from emg_agent.quality import check_quality


@tool
def answer_from_documents(question: str) -> str:
    """Answer questions about EMG reporting guidelines, the EMG Physical
    Action dataset, or how this project's quality checks work.
    Returns an answer with citations."""
    result = answer_question(question)
    return result["answer"]


@tool
def check_recording(path: str) -> str:
    """Check the signal quality of one EMG recording file (a .txt file
    in data/raw). Returns the problems found in each channel."""
    emg = load_recording(path)
    report = check_quality(emg, fs=FS, line_freq=LINE_FREQ)
    return str(report)