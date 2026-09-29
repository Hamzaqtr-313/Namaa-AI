from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TenantScopedMixin, TimestampMixin


class Customer(TenantScopedMixin, TimestampMixin, Base):
    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company: Mapped[str | None] = mapped_column(String(200), nullable=True)
    customer_type: Mapped[str | None] = mapped_column(String(50), nullable=True)  # individual, business
    status: Mapped[str] = mapped_column(String(30), default="active")
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    consent_status: Mapped[str] = mapped_column(String(20), default="pending")
    consent_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
