import os

from openai import OpenAI

EMBEDDING_DEPLOYMENT = "text-embedding-3-small"
CHAT_DEPLOYMENT = "gpt-5-mini-1"


def get_client():
    """
    Create a client for Azure OpenAI, using the endpoint and key
    from the environment variables.
    """
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].strip()
    api_key = os.environ["AZURE_OPENAI_API_KEY"].strip()
    return OpenAI(base_url=endpoint.rstrip("/") + "/openai/v1/", api_key=api_key)


def embed_texts(texts):
    """
    Turn a list of texts into a list of vectors (one vector per text).
    """
    client = get_client()
    response = client.embeddings.create(model=EMBEDDING_DEPLOYMENT, input=texts)
    return [item.embedding for item in response.data]
