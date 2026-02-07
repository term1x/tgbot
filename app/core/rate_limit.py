"""Simple in-memory rate limiter for device creation."""

from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime, timedelta

from fastapi import HTTPException, status

from app.core.config import settings


class DeviceRateLimiter:
    """Limit device creation per user in-memory."""

    def __init__(self) -> None:
        self._events: dict[str, deque[datetime]] = defaultdict(deque)

    def check(self, user_key: str) -> None:
        """Raise if the user exceeded the limit."""
        now = datetime.utcnow()
        window_start = now - timedelta(hours=1)
        events = self._events[user_key]

        while events and events[0] < window_start:
            events.popleft()

        if len(events) >= settings.rate_limit_devices_per_hour:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Device creation rate limit exceeded",
            )

        events.append(now)


rate_limiter = DeviceRateLimiter()
