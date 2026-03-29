import uuid

import pytest

from unittest.mock import AsyncMock, MagicMock, patch, mock_open

from backend.services.document_service import save_document

@pytest.mark.asyncio
async def test_save_document_adds_and_commits():
    # DB add and commit must be called; document record must be returned
    db = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    tid = str(uuid.uuid4())
    with patch("os.makedirs"), patch("aiofiles.open", mock_open()):
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
    with patch("os.makedirs"), patch("aiofiles.open", mock_open()):
        with patch("backend.services.document_service.Document") as MockDoc:
            await save_document(db, tid, "doc.txt", b"data")
            call_kwargs = MockDoc.call_args.kwargs
            assert call_kwargs["tenant_id"] == uuid.UUID(tid)
