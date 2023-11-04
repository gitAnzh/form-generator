from fastapi import APIRouter, Depends

from routers.forms.models.form_mode import FormActions
from routers.forms.validators.forms_validator import FormsValidator
from routers.users.models.auth import AuthHandler

forms_router = APIRouter()
auth_handler = AuthHandler()


@forms_router.post("/create_form", tags=["Forms"])
def create_form(data: FormsValidator):
    a = FormActions(data.dict())
    return a.create_form()


@forms_router.put("/confirm_form", tags=["Forms"])
def confirm_form(referralNumber: int):
    return FormActions.confirm_form(referralNumber)



@forms_router.get("/get_forms", tags=["Forms"])
def confirm_form(auth_header=Depends(auth_handler.check_current_user_tokens)):
    user_data, header = auth_header
    return FormActions.get_forms(user_data['staff_id'])

