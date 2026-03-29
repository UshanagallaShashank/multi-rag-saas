import uuid

from sqlalchemy import update

from ..database import AsyncSessionLocal

from ..models.chunk import Chunk

from ..models.document import Document, DocStatus

from .chunker import chunk_text

from .embedder import embed_batch

async def ingest_document(ctx: dict, document_id: str, tenant_id: str, text: str) -> None:
    # ARQ worker: chunk, embed, and store vectors; mark document ready
    async with AsyncSessionLocal() as session:
        chunks = chunk_text(text)
        embeddings = await embed_batch(chunks)
        for content, emb in zip(chunks, embeddings):
            session.add(Chunk(
                tenant_id=uuid.UUID(tenant_id),
                document_id=uuid.UUID(document_id),
                content=content,
                embedding=emb,
            ))
        await session.execute(
            update(Document).where(Document.id == uuid.UUID(document_id))
            .values(status=DocStatus.ready)
        )
        await session.commit()
