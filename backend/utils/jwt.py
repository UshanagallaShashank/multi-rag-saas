from datetime import datetime, timedelta, timezone

from jose import jwt

from ..config import settings

_ALGO = "HS256"

def create_token(user_id: str, tenant_id: str, role: str) -> str:
    # Sign JWT containing user_id, tenant_id, role
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    return jwt.encode(
        {"user_id": user_id, "tenant_id": tenant_id, "role": role, "exp": expire},
        settings.jwt_secret,
        algorithm=_ALGO,
    )

def decode_token(token: str) -> dict:
    # Verify and decode JWT, raises JWTError on failure
    return jwt.decode(token, settings.jwt_secret, algorithms=[_ALGO])
