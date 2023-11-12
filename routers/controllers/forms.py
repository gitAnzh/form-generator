import base64

from fastapi import APIRouter, Depends
from fastapi import File, UploadFile
from starlette.responses import HTMLResponse

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
def get_forms(page: int, perPage: int, auth_header=Depends(auth_handler.check_current_user_tokens)):
    user_data, header = auth_header
    company_id = user_data['staff_id']
    if user_data['username'] == "admin":
        company_id = None
    return FormActions.get_forms(company_id, page, perPage)


@forms_router.post("/upload_docs", tags=["Files"])
async def upload_docs(referral_number: int, civil_iD: UploadFile = File(..., alias="civilID"),
                      company_letter: UploadFile = File(..., alias="companyLetter"),
                      academic_proof: UploadFile = File(..., alias="academicProof"),
                      payment_fee: UploadFile = File(..., alias="paymentFee"),
                      scan_page1: UploadFile = File(..., alias="scanPage1"),
                      scan_page2: UploadFile = File(..., alias="scanPage2"),
                      scan_page3: UploadFile = File(..., alias="scanPage3"),
                      scan_page4: UploadFile = File(..., alias="scanPage4"),
                      scan_page5: UploadFile = File(..., alias="scanPage5"),
                      scan_page6: UploadFile = File(..., alias="scanPage6")):
    docs = [{"name": f'{referral_number}-civilID', "path": civil_iD.content_type, "doc": await civil_iD.read()},
            {"name": f'{referral_number}-companyLetter', "path": civil_iD.content_type,
             "doc": await company_letter.read()},
            {"name": f'{referral_number}-academicInfo', "path": academic_proof.content_type,
             "doc": await academic_proof.read()},
            {"name": f'{referral_number}-paymentFee', "path": payment_fee.content_type,
             "doc": await payment_fee.read()},
            {"name": f'{referral_number}-scanFile1', "path": scan_page1.content_type, "doc": await scan_page1.read()},
            {"name": f'{referral_number}-scanFile2', "path": scan_page2.content_type, "doc": await scan_page2.read()},
            {"name": f'{referral_number}-scanFile3', "path": scan_page3.content_type, "doc": await scan_page3.read()},
            {"name": f'{referral_number}-scanFile4', "path": scan_page4.content_type, "doc": await scan_page4.read()},
            {"name": f'{referral_number}-scanFile5', "path": scan_page5.content_type, "doc": await scan_page5.read()},
            {"name": f'{referral_number}-scanFile6', "path": scan_page6.content_type, "doc": await scan_page6.read()}
            ]
    docs = Images.upload_file(docs)
    return FormActions.add_image_to_form(referral_number, docs)


@forms_router.get("/get/{filename}")
async def get_file(filename: str):
    try:
        response = Images.get_file(filename)
        # Read image data
        image_data = response.read()
        # Base64 encode the image data
        base64_data = base64.b64encode(image_data).decode("utf-8")
        # Construct the data URI
        data_uri = f"data:{response.headers['Content-Type']};base64,{base64_data}"
        # Return the data URI as HTML
        html_content = f'<img src="{data_uri}" alt="{filename}">'
        return HTMLResponse(content=html_content, status_code=200)
    except Exception as e:
        return {"error": "something went wrong"}
