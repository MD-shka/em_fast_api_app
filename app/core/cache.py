"""Module for caching queries."""

import json
from functools import wraps
from typing import Any, Awaitable, Callable

from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis

from app.core.utils import get_expiration_time


def cache(
    redis: Redis, key_builder: Callable[[Callable[..., Awaitable[Any]], tuple[Any, ...], dict[str, Any]], str]
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    """Decorator for caching queries."""

    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        """Decorator function."""

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper function."""
            key = key_builder(func, args, kwargs)
            cached = await redis.get(key)

            if cached:
                data = json.loads(cached.decode())
                return data

            result = await func(*args, **kwargs)
            data_to_cache = jsonable_encoder(result)
            expiration_time = get_expiration_time()
            await redis.set(key, json.dumps(data_to_cache))
            await redis.expireat(key, expiration_time)
            return result

        return wrapper

    return decorator
