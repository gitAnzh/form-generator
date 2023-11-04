from fastapi import APIRouter, Depends, File

from routers.forms.models.form_mode import FormActions
from routers.forms.validators.forms_validator import FormsValidator
from routers.public_models.images_model import Images
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


@forms_router.post("/upload_docs", tags=["Files"])
def upload_docs(refferal_number: int, civilID: bytes = File(...), companyLetter: bytes = File(...),
               academicProof: bytes = File(...),
               paymentFee: bytes = File(...)):
    image = Images()
    docs = [{"name": f'{refferal_number}-civil_iD', "path": refferal_number, "doc": civilID},
            {"name": f'{refferal_number}-company_letter', "path": refferal_number, "doc": companyLetter},
            {"name": f'{refferal_number}-academic_docs', "path": refferal_number, "doc": academicProof},
            {"name": f'{refferal_number}-payment_fee', "path": refferal_number, "doc": paymentFee},
            ]
    docs = image.set_doc_file(docs)
    return FormActions.add_image_to_form(refferal_number, docs)
