"""This module contains the endpoint for getting the last trading dates."""

from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_trading_service
from app.schemas.pydantic_schemas import (
    TradingBaseFilter,
    TradingDatesFilter,
    TradingDatesResponse,
    TradingDinamicsFilter,
    TradingResultResponse,
)
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


@router.get("/dynamics", response_model=TradingResultResponse)
async def get_dynamics(
    trading_filter: TradingDinamicsFilter = Depends(),
    trading_service: TradingService = Depends(get_trading_service),
) -> TradingResultResponse:
    """
    Get the trading reslts in period.

    Args:
        trading_filter: The filter criteria for retrieving trading dynamics.
        trading_service: The trading service to use.

    Returns:
        TradingResultResponse: List trading dynamics data based on the filter.
    """
    trades = await trading_service.get_dynamics(trading_filter)
    return TradingResultResponse(trades=trades)


@router.get("/trading_result", response_model=TradingResultResponse)
async def get_trading_result(
    trading_filter: TradingBaseFilter = Depends(),
    trading_service: TradingService = Depends(get_trading_service),
) -> TradingResultResponse:
    """
    Get the last unique trading results.

    Args:
        trading_filter: The filter criteria for retrieving trading results.
        trading_service: The trading service to use.

    Returns:
        TradingResultResponse: List trading results data based on the filter.
    """
    trades = await trading_service.get_trading_results(trading_filter)
    return TradingResultResponse(trades=trades)
