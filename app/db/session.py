"""This module is responsible for creating the database session."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import db_settings

DATABASE_URL = db_settings.get_db_url

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator:
    """Returns a new session."""
    async with async_session() as session:
        yield session
