from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.deps import get_current_user
from app.database import AsyncSessionLocal, set_tenant_context
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshRequest, TenantRegisterRequest, TokenPair, UserProfile
from app.schemas.common import SuccessEnvelope
from app.utils.security import create_token, decode_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=SuccessEnvelope[TokenPair], status_code=status.HTTP_201_CREATED)
async def register_tenant(payload: TenantRegisterRequest) -> SuccessEnvelope[TokenPair]:
    """Creates a new tenant and its first (owner) user. Not tenant-scoped — runs outside RLS."""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            existing = await session.execute(select(Tenant).where(Tenant.slug == payload.tenant_slug))
            if existing.scalar_one_or_none() is not None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Tenant slug already taken")

            tenant = Tenant(name=payload.tenant_name, slug=payload.tenant_slug, status="trial")
            session.add(tenant)
            await session.flush()

            await set_tenant_context(session, str(tenant.id))

            owner = User(
                tenant_id=tenant.id,
                email=payload.owner_email,
                full_name=payload.owner_full_name,
                password_hash=hash_password(payload.owner_password),
                role="owner",
                status="active",
            )
            session.add(owner)
            await session.flush()

            tokens = TokenPair(
                access_token=create_token(str(owner.id), str(tenant.id), owner.role, "access"),
                refresh_token=create_token(str(owner.id), str(tenant.id), owner.role, "refresh"),
            )

    return SuccessEnvelope(data=tokens)


@router.post("/login", response_model=SuccessEnvelope[TokenPair])
async def login(payload: LoginRequest) -> SuccessEnvelope[TokenPair]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            tenant_result = await session.execute(select(Tenant).where(Tenant.slug == payload.tenant_slug))
            tenant = tenant_result.scalar_one_or_none()
            if tenant is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

            await set_tenant_context(session, str(tenant.id))

            user_result = await session.execute(select(User).where(User.email == payload.email))
            user = user_result.scalar_one_or_none()

            if (
                user is None
                or user.password_hash is None
                or not verify_password(payload.password, user.password_hash)
                or user.status != "active"
            ):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

            from sqlalchemy import func

            user.last_login_at = func.now()

            tokens = TokenPair(
                access_token=create_token(str(user.id), str(tenant.id), user.role, "access"),
                refresh_token=create_token(str(user.id), str(tenant.id), user.role, "refresh"),
            )

    return SuccessEnvelope(data=tokens)


@router.post("/refresh", response_model=SuccessEnvelope[TokenPair])
async def refresh(payload: RefreshRequest) -> SuccessEnvelope[TokenPair]:
    token_data = decode_token(payload.refresh_token)
    if token_data is None or token_data.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    tokens = TokenPair(
        access_token=create_token(token_data["sub"], token_data["tenant_id"], token_data["role"], "access"),
        refresh_token=create_token(token_data["sub"], token_data["tenant_id"], token_data["role"], "refresh"),
    )
    return SuccessEnvelope(data=tokens)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout() -> None:
    # Refresh tokens are stateless (JWT) in Phase 0; revocation list lands with Redis session store in Phase 1.
    return None


@router.get("/me", response_model=SuccessEnvelope[UserProfile])
async def me(current_user: User = Depends(get_current_user)) -> SuccessEnvelope[UserProfile]:
    return SuccessEnvelope(data=UserProfile.model_validate(current_user))
