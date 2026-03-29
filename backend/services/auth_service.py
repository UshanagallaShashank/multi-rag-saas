from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.tenant import Tenant

from ..models.user import User, UserRole

from ..utils.hashing import hash_password, verify_password

from ..utils.jwt import create_token

async def create_user(db: AsyncSession, email: str, password: str, tenant_name: str) -> str:
    # Create tenant + owner user, return signed JWT
    tenant = Tenant(name=tenant_name)
    db.add(tenant)
    await db.flush()
    user = User(tenant_id=tenant.id, email=email, password_hash=hash_password(password), role=UserRole.owner)
    db.add(user)
    await db.commit()
    return create_token(str(user.id), str(tenant.id), user.role.value)

async def authenticate_user(db: AsyncSession, email: str, password: str) -> str | None:
    # Verify credentials, return JWT or None
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.password_hash):
        return None
    return create_token(str(user.id), str(user.tenant_id), user.role.value)
