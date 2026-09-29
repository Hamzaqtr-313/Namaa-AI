import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TenantScopedMixin, TimestampMixin


class WorkflowTemplate(TenantScopedMixin, TimestampMixin, Base):
    __tablename__ = "workflow_templates"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    trigger: Mapped[dict] = mapped_column(JSONB, nullable=False)
    steps: Mapped[list] = mapped_column(JSONB, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class WorkflowRun(TenantScopedMixin, Base):
    __tablename__ = "workflow_runs"

    template_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workflow_templates.id"), nullable=True
    )
    trigger_entity: Mapped[str | None] = mapped_column(String(50), nullable=True)
    trigger_entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="running")
    current_step: Mapped[int] = mapped_column(Integer, default=0)
    context: Mapped[dict] = mapped_column(JSONB, default=dict)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
