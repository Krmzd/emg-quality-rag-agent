from fastapi import FastAPI
from pydantic import BaseModel

from emg_agent.agent import build_agent

app = FastAPI(title="EMG Quality RAG Agent")
agent = build_agent()


class ChatRequest(BaseModel):
    message: str
    thread_id: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    config = {"configurable": {"thread_id": request.thread_id}}
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": request.message}]}, config)
        return ChatResponse(answer=result["messages"][-1].content)
    except Exception as e:
        if "content management policy" not in str(e):
            raise
        return ChatResponse(answer="Sorry, I can't help with that request.")