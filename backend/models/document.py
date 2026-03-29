import uuid
import enum

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, func

from sqlalchemy.dialects.postgresql import UUID

from ..database import Base

class DocStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    ready = "ready"
    failed = "failed"

class Document(Base):

    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)

    filename = Column(String, nullable=False)

    doc_type = Column(String)

    status = Column(Enum(DocStatus), default=DocStatus.pending)

    embedding_model = Column(String, default="text-embedding-3-small")

    created_at = Column(DateTime, server_default=func.now())
