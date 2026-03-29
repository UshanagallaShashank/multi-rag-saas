import uuid

import pytest

from unittest.mock import AsyncMock, MagicMock, patch

from backend.services.document_service import save_document

def _async_file_mock() -> AsyncMock:
    # Build an async context manager mock for aiofiles.open
    m = AsyncMock()
    m.__aenter__ = AsyncMock(return_value=m)
    m.__aexit__ = AsyncMock(return_value=False)
    return m

@pytest.mark.asyncio
async def test_save_document_adds_and_commits():
    # DB add and commit must be called; document record must be returned
    db = AsyncMock()
    tid = str(uuid.uuid4())
    with patch("os.makedirs"), patch("aiofiles.open", return_value=_async_file_mock()):
        with patch("backend.services.document_service.Document") as MockDoc:
            mock_doc = MagicMock()
            MockDoc.return_value = mock_doc
            result = await save_document(db, tid, "file.pdf", b"content")
    db.add.assert_called_once_with(mock_doc)
    db.commit.assert_called_once()
    assert result == mock_doc

@pytest.mark.asyncio
async def test_save_document_uses_tenant_id():
    # Document must be created with a UUID tenant_id, not a raw string
    db = AsyncMock()
    tid = str(uuid.uuid4())
    with patch("os.makedirs"), patch("aiofiles.open", return_value=_async_file_mock()):
        with patch("backend.services.document_service.Document") as MockDoc:
            await save_document(db, tid, "doc.txt", b"data")
            assert MockDoc.call_args.kwargs["tenant_id"] == uuid.UUID(tid)
