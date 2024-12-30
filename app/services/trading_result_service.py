"""This module implements the Services layer."""

import json
from datetime import date
from typing import Any, Sequence

from sqlalchemy import Select
from sqlalchemy.future import select

from app.core.cache import cache
from app.models.trading_result import SpimexTradingResult as Spimex
from app.repositories.trading_result_repository import TradingResultRepository
from app.schemas.pydantic_schemas import (
    TradingBaseFilter,
    TradingDinamicsFilter,
    TradingResultBase,
)


class TradingService:
    """Trading service class."""

    def __init__(
        self,
        repository: TradingResultRepository[TradingResultBase],
        date_repository: TradingResultRepository[date],
        redis,
    ):
        self.repository = repository
        self.date_repository = date_repository
        self.redis = redis

    @staticmethod
    async def __get_filtred_trading_results(
        stmt: Select[Any], trading_filter: TradingDinamicsFilter | TradingBaseFilter
    ) -> Select[Any]:
        """Get filtered trading results."""
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

        return stmt

    async def get_last_trading_dates(self, limit: int) -> Sequence[date]:
        """Get the last trading dates."""

        @cache(
            self.redis,
            key_builder=lambda func, args, kwargs: (json.dumps({"limit": kwargs["limit"]}, sort_keys=True)),
        )
        async def _fetch_data(limit: int) -> Sequence[date]:
            stmt = select(Spimex.date).distinct().order_by(Spimex.date.desc()).limit(limit)
            return await self.date_repository.execute_query(stmt)

        return await _fetch_data(limit=limit)

    async def get_dynamics(self, trading_filter: TradingDinamicsFilter) -> Sequence[TradingResultBase]:
        """Get results trading for the period."""

        @cache(
            self.redis,
            lambda func, args, kwargs: (
                json.dumps(kwargs["trading_filter"].model_dump(), sort_keys=True, default=str)
            ),
        )
        async def _fetch_data(trading_filter: TradingDinamicsFilter) -> Sequence[TradingResultBase]:
            stmt = (
                select(Spimex).order_by(Spimex.date.desc()).limit(trading_filter.limit).offset(trading_filter.offset)
            )
            stmt = await self.__get_filtred_trading_results(stmt, trading_filter)
            results = await self.repository.execute_query(stmt)
            return [TradingResultBase.model_validate(result) for result in results]

        return await _fetch_data(trading_filter=trading_filter)

    async def get_trading_results(self, trading_filter: TradingBaseFilter) -> Sequence[TradingResultBase]:
        """Get last unique trading results."""

        @cache(
            self.redis, lambda func, args, kwargs: (json.dumps(kwargs["trading_filter"].model_dump(), sort_keys=True))
        )
        async def _fetch_data(trading_filter: TradingBaseFilter) -> Sequence[TradingResultBase]:
            stmt = (
                select(Spimex)
                .distinct(Spimex.oil_id, Spimex.delivery_type_id, Spimex.delivery_basis_id)
                .order_by(Spimex.oil_id, Spimex.delivery_type_id, Spimex.delivery_basis_id)
                .limit(trading_filter.limit)
                .offset(trading_filter.offset)
            )
            stmt = await self.__get_filtred_trading_results(stmt, trading_filter)
            results = await self.repository.execute_query(stmt)
            return [TradingResultBase.model_validate(result) for result in results]

        return await _fetch_data(trading_filter=trading_filter)
