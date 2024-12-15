"""This module implements the Services layer."""

from datetime import date
from typing import Sequence

from app.repositories.trading_result_repository import TradingResultRepository


class TradingService:
    """Trading service class."""

    def __init__(self, repository: TradingResultRepository):
        self.repository = repository

    async def get_last_trading_dates(self, limit: int) -> Sequence[date]:
        """Get the last trading dates."""
        return await self.repository.get_last_trading_dates(limit)
