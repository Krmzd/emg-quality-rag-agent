from emg_agent.agent import build_agent

agent = build_agent()
config = {"configurable": {"thread_id": "chat"}}

print("EMG agent. Type 'quit' to stop.")

while True:
    question = input("\nYou: ")
    if question.strip().lower() == "quit":
        break
    result = agent.invoke({"messages": [{"role": "user", "content": question}]}, config)
    print("\nAgent:", result["messages"][-1].content)