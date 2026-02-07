"""Service for interacting with 3X-UI API."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import httpx

from app.core.config import settings


class ThreeXUIService:
    """Wrapper around 3X-UI API endpoints."""

    def __init__(self) -> None:
        self._client = httpx.Client(base_url=settings.three_x_ui_base_url, timeout=10)

    def _login(self) -> None:
        """Authenticate with 3X-UI."""
        response = self._client.post(
            "/login",
            data={"username": settings.three_x_ui_username, "password": settings.three_x_ui_password},
        )
        response.raise_for_status()

    def create_vless_client(self, uuid: str) -> str:
        """Create a VLESS client and return the VLESS link."""
        self._login()
        expires_at = int((datetime.utcnow() + timedelta(days=30)).timestamp())
        payload: dict[str, Any] = {
            "id": uuid,
            "email": f"{uuid}@vpn",
            "expiryTime": expires_at,
            "totalGB": 50,
            "enable": True,
        }
        response = self._client.post("/panel/api/inbounds/addClient", json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("obj", {}).get("link", f"vless://{uuid}@example.com")
