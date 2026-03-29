from typing import AsyncGenerator

from .llm_openai import stream_openai

from .llm_gemini import stream_gemini

async def stream_answer(
    query: str, context: str, model: str = "gemini-1.5-flash"
) -> AsyncGenerator[str, None]:
    # Route to Gemini for gemini-* models, OpenAI for everything else
    if model.startswith("gemini"):
        async for token in stream_gemini(query, context, model):
            yield token
    else:
        async for token in stream_openai(query, context, model):
            yield token
