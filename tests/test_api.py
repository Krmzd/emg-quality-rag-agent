from types import SimpleNamespace

from fastapi.testclient import TestClient

from emg_agent import api

client = TestClient(api.app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


class FakeAgent:
    def invoke(self, inputs, config):
        return {"messages": [SimpleNamespace(content="Fake answer")]}


def test_chat_returns_agent_answer(monkeypatch):
    monkeypatch.setattr(api, "agent", FakeAgent())
    response = client.post("/chat", json={"message": "Hello", "thread_id": "t1"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Fake answer"}

def test_chat_rejects_missing_thread_id():
    response = client.post("/chat", json={"message": "Hello"})
    assert response.status_code == 422