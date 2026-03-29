import asyncio

from database import Base, engine

from models import tenant, user, document, chunk

async def main():
    # Create all tables from SQLAlchemy models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")

asyncio.run(main())
