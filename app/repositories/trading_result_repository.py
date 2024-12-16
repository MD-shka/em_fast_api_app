"""Module is Repository pattern. It is used to interact with the database."""

from datetime import date
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.trading_result import SpimexTradingResult as Spimex
from app.schemas.pydantic_schemas import (
    TradingBaseFilter,
    TradingDinamicsFilter,
    TradingResultBase,
)


class TradingResultRepository:
    """Class is used to interact with the database."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __get_filtred_trading_results(
        self, stmt: Select, trading_filter: TradingDinamicsFilter | TradingBaseFilter
    ) -> Sequence[TradingResultBase]:
        """Method is used to get filtered trading results from the database."""
        if trading_filter.oil_id:
            stmt = stmt.filter(Spimex.oil_id == trading_filter.oil_id)
        if trading_filter.delivery_type_id:
            stmt = stmt.filter(Spimex.delivery_type_id == trading_filter.delivery_type_id)
        if trading_filter.delivery_basis_id:
            stmt = stmt.filter(Spimex.delivery_basis_id == trading_filter.delivery_basis_id)
        if hasattr(trading_filter, "start_date") and trading_filter.start_date:
            stmt = stmt.filter(Spimex.date >= trading_filter.start_date)
        if hasattr(trading_filter, "end_date") and trading_filter.end_date:
            stmt = stmt.filter(Spimex.date <= trading_filter.end_date)

        result = await self.session.execute(stmt)
        trades = result.scalars().all()
        return [TradingResultBase.model_validate(trade) for trade in trades]

    async def get_last_trading_dates(self, limit: int) -> Sequence[date]:
        """Method returns the last trading dates from the database."""
        stmt = select(Spimex.date).distinct().order_by(Spimex.date.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_dynamics(
        self,
        trading_filter: TradingDinamicsFilter,
    ) -> Sequence[TradingResultBase]:
        """Method returns the dynamics of the trading results from the database."""
        stmt = select(Spimex).order_by(Spimex.date.desc()).limit(trading_filter.limit).offset(trading_filter.offset)
        return await self.__get_filtred_trading_results(stmt, trading_filter)

    async def get_trading_results(
        self,
        trading_filter: TradingBaseFilter,
    ) -> Sequence[TradingResultBase]:
        """Method returns the trading results from the database."""
        stmt = (
            select(Spimex)
            .distinct(Spimex.oil_id, Spimex.delivery_type_id, Spimex.delivery_basis_id)
            .order_by(Spimex.oil_id, Spimex.delivery_type_id, Spimex.delivery_basis_id)
            .limit(trading_filter.limit)
            .offset(trading_filter.offset)
        )
        return await self.__get_filtred_trading_results(stmt, trading_filter)
