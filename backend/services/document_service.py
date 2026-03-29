import os
import uuid

import aiofiles

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.document import Document

from ..config import settings

async def save_document(
    db: AsyncSession, tenant_id: str, filename: str, content: bytes
) -> Document:
    # Write file to disk and create DB record for the document
    os.makedirs(settings.upload_dir, exist_ok=True)
    path = f"{settings.upload_dir}/{uuid.uuid4()}_{filename}"
    async with aiofiles.open(path, "wb") as f:
        await f.write(content)
    doc = Document(tenant_id=uuid.UUID(tenant_id), filename=filename)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc
