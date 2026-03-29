from typing import AsyncGenerator

import google.generativeai as genai

from ..config import settings

genai.configure(api_key=settings.gemini_api_key)

async def stream_gemini(query: str, context: str, model: str) -> AsyncGenerator[str, None]:
    # Stream answer tokens from a Gemini model
    prompt = f"Answer using only this context:\n{context}\n\nQuestion: {query}"
    m = genai.GenerativeModel(model)
    response = await m.generate_content_async(prompt, stream=True)
    async for chunk in response:
        if chunk.text:
            yield chunk.text
