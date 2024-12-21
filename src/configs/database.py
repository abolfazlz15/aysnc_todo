from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.configs.config import Settings

settings = Settings()

# Declarative Base for ORM models
class Base(DeclarativeBase):
    pass

# Initialize the engine only once
engine = create_async_engine(
    settings.database_url,
    echo=True,
    pool_size=1,
    max_overflow=0,
)

# Create a sessionmaker with the shared engine
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency to get the database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
