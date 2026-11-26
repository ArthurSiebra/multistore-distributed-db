from fastapi import FastAPI

from gateway.core.config import settings
from gateway.core.exceptions import register_exception_handlers
from gateway.routers.health import router as health_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Gateway de banco de dados distribuido "
        "do e-commerce MultiStore."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


register_exception_handlers(app)

app.include_router(health_router)