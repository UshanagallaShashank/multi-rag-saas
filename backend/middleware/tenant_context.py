from sqlalchemy import text

from sqlalchemy.ext.asyncio import AsyncSession

async def set_tenant_context(session: AsyncSession, tenant_id: str) -> None:
    # Set PostgreSQL session variable so RLS policies can use it
    await session.execute(text("SET LOCAL app.tenant_id = :tid"), {"tid": tenant_id})
