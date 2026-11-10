from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from emg_agent.llm import get_chat_model
from emg_agent.tools import answer_from_documents, check_recording

AGENT_PROMPT = """You are an assistant for EMG signal quality and EMG research reporting.

- Use answer_from_documents for questions about EMG reporting guidelines,
  the EMG Physical Action dataset, or how the quality checks work.
- Use check_recording when the user gives a recording file path and wants
  its signal quality checked.
- Do not diagnose patients or give medical advice.
- If a question is not about EMG, say you can only help with EMG questions.
- When you use answer_from_documents, give the tool's answer to the user
  as it is, with its citations like [1]. Do not add examples, numbers or
  facts that are not in the tool's answer.
"""


def build_agent():
    llm = get_chat_model()
    tools = [answer_from_documents, check_recording]
    memory = MemorySaver()
    return create_agent(llm, tools, system_prompt=AGENT_PROMPT, checkpointer=memory)