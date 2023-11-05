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
def upload_docs(referral_number: int, civil_iD: bytes = File(..., alias="civilID"),
                company_letter: bytes = File(..., alias="companyLetter"),
                academic_proof: bytes = File(..., alias="academicProof"),
                payment_fee: bytes = File(..., alias="paymentFee"),
                scan_page1: bytes = File(..., alias="scanPage1"),
                scan_page2: bytes = File(..., alias="scanPage2"),
                scan_page3: bytes = File(..., alias="scanPage3"),
                scan_page4: bytes = File(..., alias="scanPage4"),
                scan_page5: bytes = File(..., alias="scanPage5"),
                scan_page6: bytes = File(..., alias="scanPage6")):
    image = Images()
    docs = [{"name": f'{referral_number}-civilID', "path": referral_number, "doc": civil_iD},
            {"name": f'{referral_number}-companyLetter', "path": referral_number, "doc": company_letter},
            {"name": f'{referral_number}-academicInfo', "path": referral_number, "doc": academic_proof},
            {"name": f'{referral_number}-paymentFee', "path": referral_number, "doc": payment_fee},
            {"name": f'{referral_number}-scanFile1', "path": referral_number, "doc": scan_page1},
            {"name": f'{referral_number}-scanFile2', "path": referral_number, "doc": scan_page2},
            {"name": f'{referral_number}-scanFile3', "path": referral_number, "doc": scan_page3},
            {"name": f'{referral_number}-scanFile4', "path": referral_number, "doc": scan_page4},
            {"name": f'{referral_number}-scanFile5', "path": referral_number, "doc": scan_page5},
            {"name": f'{referral_number}-scanFile6', "path": referral_number, "doc": scan_page6},
            ]
    docs = image.set_doc_file(docs)
    return FormActions.add_image_to_form(referral_number, docs)
