from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    debug: bool = True
    secret_key: str = "change-me-to-a-random-64-char-string"

    # Runtime app connection — a restricted, non-superuser role so RLS actually
    # applies (Postgres superusers and table owners bypass RLS by default).
    database_url: str = "postgresql+asyncpg://namaa_app:namaa_app_dev_password@localhost:5432/namaa"
    # Admin/owner connection, used only for running migrations (DDL, role/grant setup).
    database_url_admin: str = "postgresql+asyncpg://namaa:namaa@localhost:5432/namaa"

    redis_url: str = "redis://localhost:6379/0"

    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str = "minio"
    s3_secret_key: str = "minio123"
    s3_bucket: str = "namaa-documents"
    s3_region: str = "us-east-1"

    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    openai_api_key: str = ""
    anthropic_api_key: str = ""
    llm_primary_provider: str = "openai"
    llm_fallback_provider: str = "anthropic"

    whatsapp_phone_number_id: str = ""
    whatsapp_waba_id: str = ""
    whatsapp_access_token: str = ""
    whatsapp_app_secret: str = ""
    whatsapp_webhook_verify_token: str = "change-me"

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    imap_host: str = ""
    imap_port: int = 993

    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    unifonic_app_sid: str = ""

    fcm_server_key: str = ""

    credentials_encryption_key: str = "change-me-32-byte-base64-key-for-fernet"

    cors_origins: list[str] = ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
