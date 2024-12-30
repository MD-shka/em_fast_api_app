"""Test the cache decorator"""

import json

import pytest

from app.core.cache import cache


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filters, cached_data, expected_result, expected_key",
    [
        ({"key": "value"}, {"data": "cached"}, {"data": "cached"}, "simply_func:{'key': 'value'}"),
        ({"key": "value"}, None, {"data": "new"}, "simply_func:{'key': 'value'}"),
        (None, None, {"data": "original"}, "simply_func:None"),
    ],
)
async def test_cache_decorator(mocker, filters, cached_data, expected_result, expected_key):
    mock_redis = mocker.AsyncMock()

    if cached_data:
        mock_redis.get.return_value = json.dumps(cached_data).encode()
    else:
        mock_redis.get.return_value = None

    mocker.patch("app.core.cache.get_expiration_time", return_value=1234567890)

    def test_key_builder(func, args, kwargs):
        return f"{func.__name__}:{kwargs.get('filters', None)}"

    @cache(redis=mock_redis, key_builder=test_key_builder)
    async def simply_func(filters: dict[str, str] | None = None) -> dict[str, str]:
        """Base examples function"""
        return {"data": "new" if filters else "original"}

    result = await simply_func(filters=filters)

    assert result == expected_result
    mock_redis.get.assert_awaited_once_with(expected_key)

    if not cached_data:
        mock_redis.set.assert_awaited_once_with(expected_key, json.dumps(expected_result))
        mock_redis.expireat.assert_awaited_once_with(expected_key, 1234567890)
    else:
        mock_redis.set.assert_not_called()
        mock_redis.expireat.assert_not_called()
