from datetime import datetime

from sqlalchemy import DateTime, LargeBinary, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TenantScopedMixin, TimestampMixin


class Integration(TenantScopedMixin, TimestampMixin, Base):
    __tablename__ = "integrations"
    __table_args__ = (UniqueConstraint("tenant_id", "type", name="uq_integrations_tenant_type"),)

    type: Mapped[str] = mapped_column(String(50), nullable=False)  # whatsapp, email, calendar, crm, accounting
    config: Mapped[dict] = mapped_column(JSONB, nullable=False)
    credentials_enc: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="disconnected")
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
