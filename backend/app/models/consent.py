import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import INET, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TenantScopedMixin


class ConsentRecord(TenantScopedMixin, Base):
    __tablename__ = "consent_records"

    customer_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True
    )
    channel: Mapped[str | None] = mapped_column(String(30), nullable=True)  # whatsapp, email, sms, all
    consent_type: Mapped[str | None] = mapped_column(String(50), nullable=True)  # marketing, service, data_processing
    consent_given: Mapped[bool] = mapped_column(Boolean, nullable=False)
    consent_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    withdrawal_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(INET, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
