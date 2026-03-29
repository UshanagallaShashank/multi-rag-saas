from sqlalchemy import text

from sqlalchemy.ext.asyncio import AsyncSession

async def retrieve_chunks(
    session: AsyncSession,
    tenant_id: str,
    query_embedding: list[float],
    top_k: int = 20,
) -> list:
    # Retrieve top-k chunks by cosine similarity, filtered by tenant
    sql = text("""
        SELECT id, tenant_id, document_id, content, page_number, chunk_metadata
        FROM chunks
        WHERE tenant_id = :tenant_id
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :top_k
    """)
    result = await session.execute(
        sql, {"tenant_id": tenant_id, "embedding": str(query_embedding), "top_k": top_k}
    )
    return result.fetchall()
