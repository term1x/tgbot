"""Device endpoints."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.rate_limit import rate_limiter
from app.db import get_db
from app.models import Device, User
from app.schemas import DeviceResponse
from app.services.three_x_ui import ThreeXUIService

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("", response_model=list[DeviceResponse])
def list_devices(current_user: User = Depends(get_current_user)) -> list[DeviceResponse]:
    """List devices for current user."""
    return current_user.devices


@router.post("", response_model=DeviceResponse)
def create_device(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DeviceResponse:
    """Create a new VPN device."""
    rate_limiter.check(str(current_user.id))

    device_uuid = str(uuid4())
    service = ThreeXUIService()
    try:
        vless_link = service.create_vless_client(device_uuid)
    except Exception as exc:  # noqa: BLE001 - surface consistent API error
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="VPN provider error") from exc

    device = Device(user_id=current_user.id, uuid=device_uuid, vless_link=vless_link)
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@router.delete("/{device_id}")
def disable_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Disable a device."""
    device = db.query(Device).filter(Device.id == device_id, Device.user_id == current_user.id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

    device.active = False
    db.commit()
    return {"status": "disabled"}
