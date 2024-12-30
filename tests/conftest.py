"""Create a fixture for testing app"""

import asyncio
from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.session import get_session
from app.dependencies import get_redis_client
from app.main import app
from app.models.trading_result import Base, SpimexTradingResult
from tests.config import test_settings
from tests.fixtures.database import TRADING_RESULT

test_engine = create_async_engine(test_settings.get_db_url)
TestingSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for testing."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def test_db():
    async with test_engine.begin() as conn:
        table_exists = await conn.run_sync(
            lambda sync_conn: sync_conn.execute(
                text(
                    "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'spimex_trading_result')"
                )
            ).scalar()
        )
        if not table_exists:
            await conn.run_sync(Base.metadata.create_all)

            async with TestingSessionLocal() as session:
                for result in TRADING_RESULT:
                    if "date" in result:
                        result["date"] = datetime.strptime(result["date"], "%Y-%m-%d").date()
                    if "created_on" in result:
                        result["created_on"] = datetime.strptime(result["created_on"], "%Y-%m-%d %H:%M:%S.%f")
                    if "updated_on" in result:
                        result["updated_on"] = datetime.strptime(result["updated_on"], "%Y-%m-%d %H:%M:%S.%f")
                    trading_result = SpimexTradingResult(**result)
                    session.add(trading_result)
                await session.commit()
    yield


@pytest.fixture(scope="function")
async def db_session():
    """Create a new database session for each test function."""
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def redis_client():
    """Create a test Redis client"""
    redis = Redis.from_url(test_settings.get_redis_url)
    yield redis
    await redis.close()


@pytest.fixture
async def async_client(db_session, redis_client):
    """Create an asynchronous test client"""

    async def override_get_session():
        """Override the get_session fixture to return the db_session"""
        yield db_session

    async def override_redis_client():
        """Override the get_redis_client fixture to return the redis_client"""
        return redis_client

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_redis_client] = override_redis_client
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
