from fastapi import FastAPI

app = FastAPI(title = "EMG Quality RAG Agent")

@app.get("/health")

def health():
    return {"status": "ok"}