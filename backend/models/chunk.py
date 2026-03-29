import uuid

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func

from sqlalchemy.dialects.postgresql import UUID, JSONB

from pgvector.sqlalchemy import Vector

from ..database import Base

class Chunk(Base):

    __tablename__ = "chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)

    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)

    content = Column(String, nullable=False)

    embedding = Column(Vector(1536))

    page_number = Column(Integer)

    chunk_metadata = Column(JSONB, default={})

    created_at = Column(DateTime, server_default=func.now())
