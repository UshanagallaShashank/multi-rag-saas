from uuid import UUID

from datetime import datetime

from pydantic import BaseModel

class DocumentResponse(BaseModel):

    model_config = {"from_attributes": True}

    id: UUID

    tenant_id: UUID

    filename: str

    status: str

    created_at: datetime

class UploadResponse(BaseModel):
    document_id: UUID
    job_id: str
    status: str
