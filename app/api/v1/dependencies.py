"""This module contains the dependencies for the FastAPI application."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.trading_result_repository import TradingResultRepository
from app.services.trading_result_service import TradingService


def get_trading_service(db: AsyncSession = Depends(get_session)) -> TradingService:
    """Returns an instance of the TradingService class."""
    repository = TradingResultRepository(db)
    return TradingService(repository=repository)
