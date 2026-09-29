from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Meta(BaseModel):
    page: int = 1
    per_page: int = 50
    total: int = 0
    has_more: bool = False


class SuccessEnvelope(BaseModel, Generic[T]):
    success: bool = True
    data: T
    meta: Meta | None = None


class ErrorDetail(BaseModel):
    field: str | None = None
    issue: str


class ErrorBody(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] | None = None


class ErrorEnvelope(BaseModel):
    success: bool = False
    error: ErrorBody


def error_response(code: str, message: str, details: list[dict[str, Any]] | None = None) -> dict:
    return ErrorEnvelope(
        error=ErrorBody(code=code, message=message, details=details or None)
    ).model_dump(exclude_none=True)
