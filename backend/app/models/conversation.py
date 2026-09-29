import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TenantScopedMixin, TimestampMixin


class Conversation(TenantScopedMixin, TimestampMixin, Base):
    __tablename__ = "conversations"

    customer_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True
    )
    channel: Mapped[str] = mapped_column(String(30), nullable=False)  # whatsapp, email, web_chat, social
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="open")
    assigned_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    priority: Mapped[str] = mapped_column(String(20), default="normal")
    intent: Mapped[str | None] = mapped_column(String(100), nullable=True)
    context: Mapped[dict] = mapped_column(JSONB, default=dict)
    ai_draft: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    last_message_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
