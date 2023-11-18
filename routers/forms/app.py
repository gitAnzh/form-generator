from fastapi import FastAPI, responses
from starlette.exceptions import HTTPException as starletteHTTPException

from routers.config import settings

from routers.forms.controllers.forms import forms_router

TAGS = [
    {
        "name": "FormGenerator",
        "description": "form generator CRUD"
    }
]

app = FastAPI(
    title="Form Generator API",
    description="This is form generator service",
    version="0.1.0",
    openapi_tags=TAGS,
    docs_url="/docs/" if settings.DEBUG_MODE else None,
    redoc_url="/redoc/" if settings.DEBUG_MODE else None,
    debug=settings.DEBUG_MODE
)

app.include_router(forms_router)


# customize exception handler of fast api
@app.exception_handler(starletteHTTPException)
def validation_exception_handler(request, exc):
    return responses.JSONResponse(exc.detail, status_code=exc.status_code)
