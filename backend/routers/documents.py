from fastapi import APIRouter, Depends, UploadFile, File

from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db

from ..middleware.auth_middleware import get_current_user

from ..services.document_service import save_document

from ..schemas.document import UploadResponse

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    # Save file, create document record, enqueue ingestion job
    content = await file.read()
    doc = await save_document(db, user["tenant_id"], file.filename, content)
    return UploadResponse(document_id=doc.id, job_id=f"job_{doc.id}", status="pending")
