from typing import AsyncGenerator

from openai import AsyncOpenAI

from ..config import settings

_client = AsyncOpenAI(api_key=settings.openai_api_key)

async def stream_openai(query: str, context: str, model: str) -> AsyncGenerator[str, None]:
    # Stream answer tokens from an OpenAI chat model
    messages = [
        {"role": "system", "content": f"Answer using only this context:\n{context}"},
        {"role": "user", "content": query},
    ]
    stream = await _client.chat.completions.create(
        model=model, messages=messages, stream=True
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
