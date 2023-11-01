from fastapi import APIRouter

from routers.forms.models.form_mode import FormActions
from routers.forms.validators.forms_validator import FormsValidator
from routers.users.models.auth import AuthHandler

forms_router = APIRouter()
auth_handler = AuthHandler()


@forms_router.post("/create_form", tags=["Forms"])
def create_form(data: FormsValidator):
    a = FormActions(data.dict())
    return a.create_form()
