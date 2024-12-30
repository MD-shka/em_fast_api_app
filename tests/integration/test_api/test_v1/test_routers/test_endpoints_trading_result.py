import pytest
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


async def test_get_last_trading_dates_with_invalid_limit(async_client: AsyncClient) -> None:
    limit = -1
    response = await async_client.get(f"/api/v1/last_trading_dates?limit={limit}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert data["detail"][0]["msg"] == "Input should be greater than 0"


@pytest.mark.parametrize(
    "start_date, end_date, page, per_page",
    [
        ("2024-12-02", "2024-12-13", 1, 10),
        ("2024-12-03", "2024-12-06", 1, 5),
        ("2024-12-09", "2024-12-11", 1, 10),
        ("2024-12-09", "2024-12-09", 1, 10),
    ],
)
async def test_get_dynamics(
    async_client: AsyncClient, start_date: str, end_date: str, page: int, per_page: int
) -> None:
    url = f"/api/v1/dynamics?page={page}&per_page={per_page}&start_date={start_date}&end_date={end_date}"
    response = await async_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, dict)
    assert "trades" in data
    trades = data["trades"]
    assert isinstance(trades, list)

    assert len(trades) <= per_page

    for item in trades:
        assert isinstance(item["exchange_product_id"], str)
        assert isinstance(item["exchange_product_name"], str)
        assert isinstance(item["oil_id"], str)
        assert isinstance(item["delivery_basis_id"], str)
        assert isinstance(item["delivery_basis_name"], str)
        assert isinstance(item["delivery_type_id"], str)
        assert isinstance(item["volume"], int)
        assert isinstance(item["total"], int)
        assert isinstance(item["count"], int)
        assert isinstance(item["date"], str)

        assert start_date <= item["date"] <= end_date

    dates = [item["date"] for item in trades]
    assert dates == sorted(dates, reverse=True)


@pytest.mark.parametrize(
    "page, per_page, oil_id, delivery_type_id, delivery_basis_id",
    [
        (1, 10, "A100", "A", "PUN"),
        (1, 10, "A592", "A", "ACH"),
        (1, 10, "A100", None, None),
        (1, 10, None, "A", None),
    ],
)
async def test_get_trading_result(
    async_client: AsyncClient, page: int, per_page: int, oil_id: str, delivery_type_id: str, delivery_basis_id: str
) -> None:
    url = f"/api/v1/trading_result?page={page}&per_page={per_page}"

    if oil_id is not None:
        url += f"&oil_id={oil_id}"
    if delivery_type_id is not None:
        url += f"&delivery_type_id={delivery_type_id}"
    if delivery_basis_id is not None:
        url += f"&delivery_basis_id={delivery_basis_id}"
    response = await async_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, dict)
    assert "trades" in data
    trades = data["trades"]
    assert isinstance(trades, list)
    assert len(trades) <= per_page

    for trade in trades:
        if oil_id is not None:
            assert trade["oil_id"] == oil_id
        if delivery_type_id is not None:
            assert trade["delivery_type_id"] == delivery_type_id
        if delivery_basis_id is not None:
            assert trade["delivery_basis_id"] == delivery_basis_id
