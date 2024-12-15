"""This module contains the endpoint for getting the last trading dates."""

from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_trading_service
from app.schemas.pydantic_schemas import TradingDatesFilter, TradingDatesResponse
from app.services.trading_result_service import TradingService

router = APIRouter()


@router.get("/last_trading_dates", response_model=TradingDatesResponse)
async def get_last_trading_dates(
    limit: TradingDatesFilter = Depends(),
    trading_service: TradingService = Depends(get_trading_service),
) -> TradingDatesResponse:
    """
    Get the last trading dates.

    Args:

        limit: The limit of the last trading dates to return.
        trading_service: The trading service to use.

    Returns:

        TradingDatesResponse: List of the last trading dates.
    """
    dates = await trading_service.get_last_trading_dates(limit.limit)
    return TradingDatesResponse(dates=dates)
