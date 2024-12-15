"""Module is Repository pattern. It is used to interact with the database."""

from datetime import date
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.trading_result import SpimexTradingResult


class TradingResultRepository:
    """Class is used to interact with the database."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_last_trading_dates(self, limit: int) -> Sequence[date]:
        """Method returns the last trading dates from the database."""
        stmt = select(SpimexTradingResult.date).distinct().order_by(SpimexTradingResult.date.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_dynamics(
        self,
        oil: str | None = None,
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> Sequence[SpimexTradingResult]:
        """Method returns the dynamics of the trading results from the database."""
        pass
