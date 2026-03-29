import uuid
import enum

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, func

from sqlalchemy.dialects.postgresql import UUID

from ..database import Base

class UserRole(str, enum.Enum):
    owner = "owner"
    admin = "admin"
    viewer = "viewer"

class User(Base):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)

    email = Column(String, unique=True, nullable=False)

    password_hash = Column(String, nullable=False)

    role = Column(Enum(UserRole), default=UserRole.owner)

    created_at = Column(DateTime, server_default=func.now())
