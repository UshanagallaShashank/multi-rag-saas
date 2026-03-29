from sqlalchemy import Column, String, Boolean, DateTime, func

from sqlalchemy.dialects.postgresql import UUID

import uuid

from ..database import Base

class Tenant(Base):

    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
