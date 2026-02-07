"""Pydantic schemas."""

from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: str
    username: str | None
    balance: Decimal
    created_at: datetime


class DeviceResponse(BaseModel):
    """Device response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: str
    vless_link: str
    active: bool
    created_at: datetime


class PaymentCreate(BaseModel):
    """Mock top-up request."""

    amount: Decimal


class PaymentResponse(BaseModel):
    """Payment response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: Decimal
    status: str
    created_at: datetime
