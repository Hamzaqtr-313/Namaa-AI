from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal, set_tenant_context
from app.models.user import User
from app.utils.security import decode_token

bearer_scheme = HTTPBearer(auto_error=False)


class AuthContext:
    def __init__(self, user_id: str, tenant_id: str, role: str):
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.role = role


async def get_auth_context(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> AuthContext:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")

    payload = decode_token(credentials.credentials)
    if payload is None or payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return AuthContext(user_id=payload["sub"], tenant_id=payload["tenant_id"], role=payload["role"])


async def get_tenant_db(
    auth: AuthContext = Depends(get_auth_context),
) -> AsyncGenerator[AsyncSession, None]:
    """A DB session scoped to the authenticated user's tenant via RLS.

    SET LOCAL only holds for the current transaction, so the transaction must
    stay open for the lifetime of the request — commit happens on clean exit,
    rollback on exception.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await set_tenant_context(session, auth.tenant_id)
            yield session


async def get_current_user(
    auth: AuthContext = Depends(get_auth_context),
    db: AsyncSession = Depends(get_tenant_db),
) -> User:
    result = await db.execute(select(User).where(User.id == auth.user_id))
    user = result.scalar_one_or_none()
    if user is None or user.status != "active":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
    return user
