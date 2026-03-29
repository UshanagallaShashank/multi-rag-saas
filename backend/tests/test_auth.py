import pytest

from unittest.mock import AsyncMock, MagicMock, patch

from backend.services.auth_service import create_user, authenticate_user

@pytest.mark.asyncio
async def test_create_user_returns_token():
    # Should call db.flush + commit and return a JWT string
    db = AsyncMock()
    db.flush = AsyncMock()
    db.commit = AsyncMock()
    with patch("backend.services.auth_service.create_token", return_value="jwt123"):
        token = await create_user(db, "user@test.com", "pass", "Acme")
    assert token == "jwt123"
    db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_authenticate_unknown_user_returns_none():
    # Non-existent user must return None, never raise
    db = AsyncMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=None)))
    result = await authenticate_user(db, "nobody@x.com", "pass")
    assert result is None

@pytest.mark.asyncio
async def test_authenticate_wrong_password_returns_none():
    # Correct user but wrong password must return None
    db = AsyncMock()
    fake_user = MagicMock()
    fake_user.password_hash = "hashed"
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=fake_user)))
    with patch("backend.services.auth_service.verify_password", return_value=False):
        result = await authenticate_user(db, "user@x.com", "wrong")
    assert result is None
