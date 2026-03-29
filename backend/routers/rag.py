from fastapi import APIRouter, Depends

from fastapi.responses import StreamingResponse

from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel

from ..database import get_db

from ..services.embedder import embed_one

from ..services.retriever import retrieve_chunks

from ..services.reranker import rerank

from ..services.llm_router import stream_answer

router = APIRouter(prefix="/v1/rag", tags=["rag"])

class QueryRequest(BaseModel):
    query: str

@router.post("/{tenant_id}/query")
async def rag_query(tenant_id: str, body: QueryRequest, db: AsyncSession = Depends(get_db)):
    # Embed → retrieve top-20 → rerank to top-5 → stream LLM answer
    embedding = await embed_one(body.query)
    chunks = await retrieve_chunks(db, tenant_id, embedding)
    top = rerank(body.query, chunks)
    context = "\n\n".join(c.content for c in top)
    return StreamingResponse(stream_answer(body.query, context), media_type="text/event-stream")
