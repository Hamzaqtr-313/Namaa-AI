import uuid
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.database_url, pool_pre_ping=True, echo=settings.debug)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yields a session with app.tenant_id already set for RLS, when present in request state."""
    async with AsyncSessionLocal() as session:
        yield session


async def set_tenant_context(session: AsyncSession, tenant_id: str) -> None:
    """Sets the Postgres session variable that RLS policies filter on.

    Must run inside the same transaction as the queries that follow it,
    since SET LOCAL is scoped to the current transaction. SET LOCAL doesn't
    accept bound parameters, so the value is validated as a UUID (rejecting
    anything else) and then inlined — safe because a UUID can't break out
    of the string literal.
    """
    from sqlalchemy import text

    validated = uuid.UUID(str(tenant_id))
    await session.execute(text(f"SET LOCAL app.tenant_id = '{validated}'"))
