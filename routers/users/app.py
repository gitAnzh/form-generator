from fastapi import FastAPI, responses
from starlette.exceptions import HTTPException as starletteHTTPException

from routers.config import settings
from routers.users.controllers.users import user_router

TAGS = [
    {
        "name": "Order",
        "description": "ORDER CRUD"
    }
]

appd = FastAPI(
    title="Order API",
    description="This is users gateway MicroService",
    version="0.1.0",
    openapi_tags=TAGS,
    docs_url="/docs/" if settings.DEBUG_MODE else None,
    redoc_url="/redoc/" if settings.DEBUG_MODE else None,
    debug=settings.DEBUG_MODE
)


appd.include_router(user_router)


# customize exception handler of fast api
@appd.exception_handler(starletteHTTPException)
def validation_exception_handler(request, exc):
    return responses.JSONResponse(exc.detail, status_code=exc.status_code)
