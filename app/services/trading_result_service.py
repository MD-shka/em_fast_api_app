"""This module implements the Services layer."""

from datetime import date
from typing import Sequence

from app.repositories.trading_result_repository import TradingResultRepository
from app.schemas.pydantic_schemas import (
    TradingBaseFilter,
    TradingDinamicsFilter,
    TradingResultBase,
)


class TradingService:
    """Trading service class."""

    def __init__(self, repository: TradingResultRepository):
        self.repository = repository

    async def get_last_trading_dates(self, limit: int) -> Sequence[date]:
        """Get the last trading dates."""
        return await self.repository.get_last_trading_dates(limit)

    async def get_dynamics(self, trading_filter: TradingDinamicsFilter) -> Sequence[TradingResultBase]:
        """Get results trading for the period."""
        return await self.repository.get_dynamics(trading_filter)

    async def get_trading_results(self, trading_filter: TradingBaseFilter) -> Sequence[TradingResultBase]:
        """Get last unique trading results."""
        return await self.repository.get_trading_results(trading_filter)
