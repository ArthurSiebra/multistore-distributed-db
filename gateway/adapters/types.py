from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Generic, TypeVar


T = TypeVar("T")

Record = dict[str, Any]

Filters = dict[str, Any]


class FilterOperator(StrEnum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"


class ErrorCode(StrEnum):
    CONNECTION_ERROR = "CONNECTION_ERROR"
    FRAGMENT_NOT_FOUND = "FRAGMENT_NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    DUPLICATE_KEY = "DUPLICATE_KEY"
    RECORD_NOT_FOUND = "RECORD_NOT_FOUND"
    DATABASE_ERROR = "DATABASE_ERROR"
    PARTIAL_FAILURE = "PARTIAL_FAILURE"


@dataclass
class AdapterError:
    codigo: ErrorCode
    mensagem: str


@dataclass
class AdapterResult(Generic[T]):
    sucesso: bool
    dados: T | None = None
    total: int = 0
    erro: AdapterError | None = None

    @classmethod
    def success(
        cls,
        dados: T | None = None,
        total: int = 0
    ) -> "AdapterResult[T]":

        return cls(
            sucesso=True,
            dados=dados,
            total=total,
            erro=None
        )

    @classmethod
    def failure(
        cls,
        codigo: ErrorCode,
        mensagem: str
    ) -> "AdapterResult[T]":

        return cls(
            sucesso=False,
            dados=None,
            total=0,
            erro=AdapterError(
                codigo=codigo,
                mensagem=mensagem
            )
        )
