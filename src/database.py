from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import AsyncGenerator
from config import Settings

settings = Settings()

# Use only DeclarativeBase
class Base(DeclarativeBase):
    pass

def get_engine():
    engine = create_async_engine(
        settings.database_url,
        echo=True,
        pool_size=1,
        max_overflow=0,
    )
    return engine

# Use the shared engine for sessions
async_session = sessionmaker(
    get_engine(), class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
