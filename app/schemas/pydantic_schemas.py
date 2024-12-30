"""Pydantic schemas for the trading results API."""

from datetime import date
from typing import Annotated, Sequence

from fastapi import Query
from pydantic import BaseModel, model_validator


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

    model_config = {"from_attributes": True}


class TradingResultResponse(BaseModel):
    trades: Sequence[TradingResultBase]


class TradingDatesFilter(BaseModel):
    limit: Annotated[int, Query(gt=0)] = 10


class TradingDatesResponse(BaseModel):
    dates: Sequence[date]


class Pagination(BaseModel):
    page: Annotated[int, Query(gt=0)] = 1
    per_page: Annotated[int, Query(gt=0, le=100)] = 100

    @property
    def offset(self) -> int:
        """Return the offset for the query."""
        return (self.page - 1) * self.per_page

    @property
    def limit(self) -> int:
        """Return the limit for the query."""
        return self.per_page


class TradingBaseFilter(Pagination):
    oil_id: Annotated[str | None, Query()] = None
    delivery_type_id: Annotated[str | None, Query()] = None
    delivery_basis_id: Annotated[str | None, Query()] = None


class TradingDinamicsFilter(TradingBaseFilter):
    start_date: Annotated[date, Query()] = date.today()
    end_date: Annotated[date, Query()] = date.today()

    @model_validator(mode="before")
    @classmethod
    def validate_dates(cls, values: dict[str, date]) -> dict[str, date]:
        """Validate start_date and end_date."""
        start_date = values.get("start_date")
        end_date = values.get("end_date")
        if end_date < start_date:  # type: ignore
            raise ValueError("end_date must be greater than start_date")
        return values
