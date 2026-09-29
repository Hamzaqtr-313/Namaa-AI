from sqlalchemy import Boolean, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TenantScopedMixin, TimestampMixin


class CatalogItem(TenantScopedMixin, TimestampMixin, Base):
    __tablename__ = "catalog_items"

    name: Mapped[str] = mapped_column(String(300), nullable=False)
    name_ar: Mapped[str | None] = mapped_column(String(300), nullable=True)
    sku: Mapped[str | None] = mapped_column(String(100), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="QAR")
    unit: Mapped[str] = mapped_column(String(30), default="piece")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
