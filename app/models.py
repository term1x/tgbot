"""Database models."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    """Telegram user model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    balance = Column(Numeric(10, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    devices = relationship("Device", back_populates="user")
    payments = relationship("Payment", back_populates="user")


class Device(Base):
    """VPN device model."""

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uuid = Column(String, unique=True, index=True, nullable=False)
    vless_link = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)

    user = relationship("User", back_populates="devices")


class Payment(Base):
    """Payment history model."""

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="payments")
