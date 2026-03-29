from fastapi import FastAPI

from slowapi import _rate_limit_exceeded_handler

from slowapi.errors import RateLimitExceeded

from .utils.rate_limiter import limiter

from .routers import auth, documents, rag

app = FastAPI(title="RAGForge")

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth.router)

app.include_router(documents.router)

app.include_router(rag.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
