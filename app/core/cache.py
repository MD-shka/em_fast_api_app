"""Module for caching queries."""

import json
from functools import wraps
from typing import Any, Awaitable, Callable

from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis  # type: ignore

from app.core.config import settings as s
from app.core.utils import get_expiration_time

redis_client: Redis = Redis.from_url(s.get_redis_url)


def cache() -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    """Decorator for caching queries."""

    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        """Decorator function."""

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper function."""
            key = f"{func.__name__}:{str(kwargs.get("filters", ""))}"
            cached = await redis_client.get(key)

            if cached:
                data = json.loads(cached.decode())
                return data

            result = await func(*args, **kwargs)
            data_to_cache = jsonable_encoder(result)
            expiration_time = get_expiration_time()
            await redis_client.set(key, json.dumps(data_to_cache))
            await redis_client.expireat(key, expiration_time)
            return result

        return wrapper

    return decorator
