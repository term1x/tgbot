"""Auth endpoints."""

import json
from typing import Any

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_telegram_init_data
from app.db import get_db
from app.models import User
from app.schemas import TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=TokenResponse)
def authenticate(init_data: str = Form(...), db: Session = Depends(get_db)) -> TokenResponse:
    """Authenticate user via Telegram init data."""
    parsed = verify_telegram_init_data(init_data)
    user_data: dict[str, Any] = json.loads(parsed.get("user", "{}"))
    telegram_id = str(user_data.get("id"))
    username = user_data.get("username")

    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
    elif username and user.username != username:
        user.username = username
        db.commit()

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)
