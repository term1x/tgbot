"""Balance endpoints."""

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db import get_db
from app.models import Payment, User
from app.schemas import PaymentCreate, PaymentResponse

router = APIRouter(prefix="/balance", tags=["balance"])


@router.post("/topup", response_model=PaymentResponse)
def top_up_balance(
    payload: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PaymentResponse:
    """Mock balance top-up."""
    amount = Decimal(payload.amount)
    payment = Payment(user_id=current_user.id, amount=amount, status="mocked")
    current_user.balance = current_user.balance + amount

    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
