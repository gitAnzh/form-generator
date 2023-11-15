import datetime

from fastapi import APIRouter, Depends, Response
from fastapi import File, UploadFile, HTTPException

from routers.database.mongo_connection import minio_client
from routers.forms.models.form_mode import FormActions, filename_creator
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
def get_forms(page: int, perPage: int, auth_header=Depends(auth_handler.check_current_user_tokens)):
    user_data, header = auth_header
    company_id = user_data['staff_id']
    if user_data['username'] == "admin":
        company_id = None
    return FormActions.get_forms(company_id, page, perPage)


@forms_router.post("/upload_docs", tags=["Files"])
async def upload_docs(referral_number: int,
                      civil_ID: UploadFile = File(..., alias="civilID"),
                      company_letter: UploadFile = File(..., alias="companyLetter"),
                      academic_proof: UploadFile = File(..., alias="academicProof"),
                      payment_fee: UploadFile = File(..., alias="paymentFee"),
                      scan_page1: UploadFile = File(..., alias="scanPage1"),
                      scan_page2: UploadFile = File(..., alias="scanPage2"),
                      scan_page3: UploadFile = File(..., alias="scanPage3"),
                      scan_page4: UploadFile = File(..., alias="scanPage4"),
                      scan_page5: UploadFile = File(..., alias="scanPage5"),
                      scan_page6: UploadFile = File(..., alias="scanPage6"),
                      ):
    start = datetime.datetime.now()
    docs_dict = {
        "civil_iD": civil_ID,
        "company_letter": company_letter,
        "academic_proof": academic_proof,
        "payment_fee": payment_fee,
        "scan_page1": scan_page1,
        "scan_page2": scan_page2,
        "scan_page3": scan_page3,
        "scan_page4": scan_page4,
        "scan_page5": scan_page5,
        "scan_page6": scan_page6,
    }
    names = []
    minio_errors = []
    for name, doc in docs_dict.items():
        filename = filename_creator(referral_number, doc, name)
        minio_response, result = minio_client.upload_file(file_name=filename, file_path=doc.file.fileno())
        if result is None:
            minio_errors.append(minio_response)
        names.append(filename)
    if len(minio_errors):
        raise HTTPException(status_code=400)
    return FormActions.add_image_to_form(referral_number, names)


@forms_router.get("/get/{filename}", tags=["Get Files"])
async def get_file(filename: str):
    try:
        response = minio_client.download_file(filename)
        return Response(content=response.read(), media_type=f"image/{filename.split('.')[-1]}")
    except Exception as e:
        return {"error": "something went wrong"}
