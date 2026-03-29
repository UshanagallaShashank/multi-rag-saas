from fastapi import HTTPException, Depends

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..utils.jwt import decode_token

_bearer = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> dict:
    # Decode Bearer JWT, return payload with user_id, tenant_id, role
    try:
        return decode_token(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
