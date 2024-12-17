"""Module for caching queries."""

import json
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Awaitable, Callable

from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis  # type: ignore

from app.core.config import settings as s

redis_client: Redis = Redis.from_url(s.get_redis_url)


def get_ttl() -> int:
    """Get the cache TTL in seconds."""
    target_time = datetime.now().replace(hour=14, minute=11, second=0, microsecond=0)
    now = datetime.now()
    ttl = (target_time + timedelta(days=1 if now > target_time else 0) - now).seconds
    return ttl


def cache(ttl: int | None = None) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    """Decorator for caching queries."""
    if ttl is None:
        ttl = get_ttl()

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
            await redis_client.set(key, json.dumps(data_to_cache), ex=ttl)
            return result

        return wrapper

    return decorator
