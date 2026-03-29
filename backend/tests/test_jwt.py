import uuid

import pytest

from backend.utils.jwt import create_token, decode_token

_UID = str(uuid.uuid4())
_TID = str(uuid.uuid4())

def test_token_roundtrip():
    # Decode should return same user_id, tenant_id, role that were encoded
    token = create_token(_UID, _TID, "owner")
    payload = decode_token(token)
    assert payload["user_id"] == _UID
    assert payload["tenant_id"] == _TID
    assert payload["role"] == "owner"

def test_invalid_token_raises():
    # A garbage string must raise on decode
    with pytest.raises(Exception):
        decode_token("not.a.real.token")

def test_tampered_token_raises():
    # Changing one char of the signature must raise
    token = create_token(_UID, _TID, "admin") + "x"
    with pytest.raises(Exception):
        decode_token(token)
