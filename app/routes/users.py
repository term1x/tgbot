"""User endpoints."""

from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.models import User
from app.schemas import UserResponse

router = APIRouter(tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Return current user profile."""
    return current_user
