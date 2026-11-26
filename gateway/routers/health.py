import logging

import psycopg2
import mysql.connector

from pymongo import MongoClient
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from gateway.core.config import settings
from gateway.schemas.response import SuccessResponse, ErrorResponse


logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])


def check_postgres() -> bool:
    try:
        connection = psycopg2.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            connect_timeout=3,
            options="-c statement_timeout=3000"
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return cursor.fetchone()[0] == 1
        finally:
            connection.close()

    except Exception:
        logger.warning("Falha na verificacao do PostgreSQL")
        return False


def check_mysql() -> bool:
    try:
        connection = mysql.connector.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            database=settings.MYSQL_DATABASE,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            connection_timeout=3
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return cursor.fetchone()[0] == 1
        finally:
            connection.close()

    except Exception:
        logger.warning("Falha na verificacao do MySQL")
        return False


def check_mongodb() -> bool:
    try:
        with MongoClient(
            host=settings.MONGO_HOST,
            port=settings.MONGO_PORT,
            username=settings.MONGO_USER,
            password=settings.MONGO_PASSWORD,
            authSource=settings.MONGO_AUTH_SOURCE,
            serverSelectionTimeoutMS=3000,
            connectTimeoutMS=3000,
            socketTimeoutMS=3000
        ) as client:
            result = client[settings.MONGO_DATABASE].command("ping")
            return result.get("ok") == 1

    except Exception:
        logger.warning("Falha na verificacao do MongoDB")
        return False


@router.get(
    "/health",
    response_model=SuccessResponse[dict[str, str]],
    responses={503: {"model": ErrorResponse}},
    summary="Verificar disponibilidade da infraestrutura"
)
def health():

    databases = {
        "postgresql": "up" if check_postgres() else "down",
        "mysql": "up" if check_mysql() else "down",
        "mongodb": "up" if check_mongodb() else "down"
    }

    if all(status == "up" for status in databases.values()):
        return SuccessResponse(
            message="Gateway operacional",
            data=databases
        )

    response = ErrorResponse(
        message="Infraestrutura parcialmente indisponivel",
        details=databases
    )

    return JSONResponse(
        status_code=503,
        content=response.model_dump(mode="json")
    )