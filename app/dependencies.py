"""This module contains the dependencies for the FastAPI application."""

from datetime import date

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_session
from app.repositories.trading_result_repository import TradingResultRepository
from app.schemas.pydantic_schemas import TradingResultBase
from app.services.trading_result_service import TradingService


async def get_redis_client() -> Redis:
    """Returns an instance of the Redis client."""
    return Redis.from_url(settings.get_redis_url)


def get_trading_service(
    db: AsyncSession = Depends(get_session), redis: Redis = Depends(get_redis_client)
) -> TradingService:
    """Returns an instance of the TradingService class."""
    repository = TradingResultRepository[TradingResultBase](db)
    date_repository = TradingResultRepository[date](db)
    return TradingService(repository=repository, date_repository=date_repository, redis=redis)
