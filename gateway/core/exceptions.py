import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from gateway.schemas.response import ErrorResponse


logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ):
        response = ErrorResponse(
            message=str(exc.detail)
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump(mode="json"),
            headers=exc.headers
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        details = [
            {
                "field": ".".join(map(str, error["loc"])),
                "message": error["msg"]
            }
            for error in exc.errors()
        ]

        response = ErrorResponse(
            message="Dados invalidos na requisicao",
            details=details
        )

        return JSONResponse(
            status_code=422,
            content=response.model_dump(mode="json")
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request, exc: Exception
    ):
        logger.error(
            "Erro interno no gateway",
            exc_info=exc
        )

        response = ErrorResponse(
            message="Erro interno do servidor"
        )

        return JSONResponse(
            status_code=500,
            content=response.model_dump(mode="json")
        )