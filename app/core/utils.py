"""Calculate expiration time for caching."""

from datetime import datetime, timedelta

CACHE_REFRESH_HOUR: int = 14
CACHE_REFRESH_MINUTE: int = 11

_next_expiration_time: int | None = None


def get_expiration_time() -> int:
    """Calculate and return the expiration time for caching."""
    global _next_expiration_time

    cur_time = datetime.now()

    if _next_expiration_time is None or cur_time.timestamp() >= _next_expiration_time:
        target_time = cur_time.replace(hour=CACHE_REFRESH_HOUR, minute=CACHE_REFRESH_MINUTE, second=0, microsecond=0)
        if cur_time > target_time:
            target_time += timedelta(days=1)
        _next_expiration_time = int(target_time.timestamp())

    return _next_expiration_time
