import pytest

from unittest.mock import AsyncMock, MagicMock

from backend.services.retriever import retrieve_chunks

@pytest.mark.asyncio
async def test_calls_db_with_tenant_filter():
    # Session.execute must be called exactly once with the SQL
    session = AsyncMock()
    mock_result = MagicMock()
    mock_result.fetchall.return_value = [MagicMock(), MagicMock()]
    session.execute = AsyncMock(return_value=mock_result)
    chunks = await retrieve_chunks(session, "tenant-abc", [0.1] * 1536, top_k=5)
    session.execute.assert_called_once()
    assert len(chunks) == 2

@pytest.mark.asyncio
async def test_returns_empty_when_no_chunks():
    session = AsyncMock()
    mock_result = MagicMock()
    mock_result.fetchall.return_value = []
    session.execute = AsyncMock(return_value=mock_result)
    chunks = await retrieve_chunks(session, "tenant-xyz", [0.0] * 1536)
    assert chunks == []
