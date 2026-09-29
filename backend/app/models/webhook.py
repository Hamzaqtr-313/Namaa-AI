from datetime import datetime

from sqlalchemy import ARRAY, Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TenantScopedMixin


class Webhook(TenantScopedMixin, Base):
    __tablename__ = "webhooks"

    url: Mapped[str] = mapped_column(String(500), nullable=False)
    event_types: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    secret: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_triggered: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failure_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
