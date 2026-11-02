import os

from openai import OpenAI

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].strip()
api_key = os.environ["AZURE_OPENAI_API_KEY"].strip()
client = OpenAI(
    base_url=endpoint.rstrip("/") + "/openai/v1/",
    api_key=api_key,
)

# 1. Embeddings
embedding_response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Surface EMG is often band-pass filtered between 20 and 450 Hz.",
)
vector = embedding_response.data[0].embedding
print("Embedding length:", len(vector))
print("First 5 numbers:", vector[:5])
print("Tokens used:", embedding_response.usage.total_tokens)
print()

# 2. Chat
chat_response = client.chat.completions.create(
    model="gpt-5-mini-1",
    messages=[
        {"role": "user", "content": "In one sentence: what is power-line noise in EMG?"},
    ],
    max_completion_tokens=1000,
)
print("Answer:", chat_response.choices[0].message.content)
print("Tokens used:", chat_response.usage.total_tokens)
