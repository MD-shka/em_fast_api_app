from fastapi import status
from httpx import AsyncClient


async def test_get_last_trading_dates_without_limit(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/last_trading_dates")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "dates" in data
    assert len(data["dates"]) > 0
    assert len(data["dates"]) == 10
    assert all(isinstance(date, str) for date in data["dates"])


async def test_get_last_trading_dates_with_limit(async_client: AsyncClient) -> None:
    limit = 3
    response = await async_client.get(f"/api/v1/last_trading_dates?limit={limit}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["dates"]) <= limit
    dates = data["dates"]
    assert dates == sorted(dates, reverse=True)
    expected_dates = ["2024-12-13", "2024-12-12", "2024-12-11"]
    assert dates == expected_dates[:limit]
