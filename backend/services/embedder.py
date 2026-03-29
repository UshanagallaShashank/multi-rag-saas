from openai import AsyncOpenAI

from ..config import settings

_client = AsyncOpenAI(api_key=settings.openai_api_key)

_MODEL = "text-embedding-3-small"

async def embed_batch(texts: list[str]) -> list[list[float]]:
    # Embed a list of texts, return list of 1536-dim vectors
    response = await _client.embeddings.create(model=_MODEL, input=texts)
    return [item.embedding for item in response.data]

async def embed_one(text: str) -> list[float]:
    # Embed a single text, return 1536-dim vector
    return (await embed_batch([text]))[0]
