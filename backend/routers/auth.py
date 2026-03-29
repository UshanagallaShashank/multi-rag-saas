from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db

from ..schemas.auth import SignupRequest, LoginRequest, TokenResponse

from ..services.auth_service import create_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=TokenResponse)
async def signup(body: SignupRequest, db: AsyncSession = Depends(get_db)):
    # Create tenant + user, return JWT
    token = await create_user(db, body.email, body.password, body.tenant_name)
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    # Verify credentials, return JWT or 401
    token = await authenticate_user(db, body.email, body.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=token)
