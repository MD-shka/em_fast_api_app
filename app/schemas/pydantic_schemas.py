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


class TradingDatesFilter(BaseModel):
    limit: Annotated[int, Query(gt=0)] = 10


class TradingDatesResponse(BaseModel):
    dates: Sequence[date]
