from typing import Any, Generic, Literal, TypeVar
from pydantic import BaseModel


T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    success: Literal[True] = True
    message: str
    data: T | None = None


class ErrorResponse(BaseModel):
    success: Literal[False] = False
    message: str
    details: Any = None