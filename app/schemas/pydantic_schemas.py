"""Pydantic schemas for the trading results API."""

from datetime import date
from typing import Annotated, Sequence

from fastapi import Query
from pydantic import BaseModel


class TradingResultBase(BaseModel):
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int
    total: int
    count: int
    date: date

    class Config:
        """Allow ORM mode."""

        from_attributes = True


class TradingDatesFilter(BaseModel):
    limit: Annotated[int, Query(gt=0)] = 10


class TradingDatesResponse(BaseModel):
    dates: Sequence[date]


class TradingBaseFilter(BaseModel):
    oil_id: Annotated[str | None, Query()] = None
    delivery_type_id: Annotated[str | None, Query()] = None
    delivery_basis_id: Annotated[str | None, Query()] = None


class TradingDinamicsFilter(TradingBaseFilter):
    start_date: Annotated[date, Query()] = date.today()
    end_date: Annotated[date, Query()] = date.today()


class TradingResultResponse(BaseModel):
    trades: Sequence[TradingResultBase]
