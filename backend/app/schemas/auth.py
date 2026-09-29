import uuid

from pydantic import BaseModel, EmailStr, Field


class TenantRegisterRequest(BaseModel):
    tenant_name: str = Field(min_length=2, max_length=200)
    tenant_slug: str = Field(min_length=2, max_length=100, pattern=r"^[a-z0-9-]+$")
    owner_full_name: str = Field(min_length=2, max_length=200)
    owner_email: EmailStr
    owner_password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    tenant_slug: str
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserProfile(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    email: str
    full_name: str
    role: str
    status: str

    model_config = {"from_attributes": True}
