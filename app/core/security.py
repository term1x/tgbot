"""Security helpers for Telegram and JWT."""

from __future__ import annotations

import base64
import hashlib
import hmac
import time
from urllib.parse import parse_qsl

import jwt
from fastapi import HTTPException, status

from app.core.config import settings


def _telegram_secret() -> bytes:
    """Create a secret key for Telegram verification."""
    return hashlib.sha256(settings.bot_token.encode()).digest()


def verify_telegram_init_data(init_data: str) -> dict[str, str]:
    """Validate Telegram WebApp init data and return parsed fields."""
    parsed = dict(parse_qsl(init_data, strict_parsing=True))
    received_hash = parsed.pop("hash", "")
    data_check = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    computed_hash = hmac.new(_telegram_secret(), data_check.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(received_hash, computed_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Telegram signature")

    return parsed


def create_access_token(subject: str) -> str:
    """Create JWT access token."""
    now = int(time.time())
    payload = {"sub": subject, "iat": now, "exp": now + settings.jwt_exp_minutes * 60}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    """Decode JWT access token."""
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
