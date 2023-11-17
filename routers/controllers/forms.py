import logging

from fastapi import APIRouter, Depends, Response, Query
from fastapi import File, UploadFile, HTTPException

from routers.database.minio_connection import minio_client
from routers.forms.models.form_mode import FormActions
from routers.forms.validators.forms_validator import FormsValidator, ReferralNumber
from routers.public_models.counter import id_counter
from routers.public_models.filename_creator import filename_creator
from routers.users.models.auth import AuthHandler

forms_router = APIRouter()
auth_handler = AuthHandler()


@forms_router.post("/create_form", tags=["Forms"])
def create_form(response: Response, data: FormsValidator):
    result = FormActions(id_counter("forms")).create_form(data.dict())
    if not result.get("success"):
        raise HTTPException(status_code=404, detail={"error": "something went wrong!"})
    response.status_code = 200
    return {"message": "Form registered successfully"}


@forms_router.put("/confirm_form", tags=["Forms"])
def confirm_form(response: Response, data: ReferralNumber):
    result = FormActions(data.referral_number).confirm_form()
    if not result.get("success"):
        raise HTTPException(status_code=404, detail={"error": "something went wrong!"})
    response.status_code = 200
    return {"message": "Form confirmed successfully"}


@forms_router.get("/get_forms", tags=["Forms"])
def get_forms(
        response: Response,
        page: int = Query(default=1, alias="page"),
        per_page: int = Query(default=15, alias="perPage"),
        auth_header=Depends(auth_handler.check_current_user_tokens)
):
    user_data, header = auth_header
    company_id = user_data['staff_id']
    if user_data.get('is_admin'):
        company_id = None
    result = FormActions.get_forms(company_id, page, per_page)
    if not result.get("success"):
        raise HTTPException(status_code=404, detail={"error": "something went wrong!"})
    response.status_code = 200
    del result["success"]
    return result


@forms_router.post("/upload_docs", tags=["Files"])
async def upload_docs(
        response: Response,
        referral_number: int,
        civil_id: UploadFile = File(..., alias="civilID"),
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
    docs_dict = {
        "civil_iD": civil_id,
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
    doc_name = []
    minio_errors = []
    for name, doc in docs_dict.items():
        filename = filename_creator(referral_number, doc, name)
        minio_response, result = minio_client.upload_file(file_name=filename, content_type=doc.content_type,
                                                          doc=await doc.read())
        if result is None:
            minio_errors.append(minio_response)
        doc_name.append(filename)
    if len(minio_errors):
        raise HTTPException(status_code=400)
    result = FormActions(referral_number).add_image_to_form(doc_name)
    if not result.get("success"):
        raise HTTPException(status_code=404, detail={"error": "something went wrong!"})
    response.status_code = 200
    return {
        "message": f"Images successfully added to form, your referral number is {referral_number}, wait for our call, "
                   f"thanks"
    }


@forms_router.get("/get_doc", tags=["Get Files"])
def get_file(filename: str = Query(...)):
    try:
        response = minio_client.download_file(filename)
        return Response(content=response.read(), media_type=f"image/{filename.split('.')[-1]}")
    except Exception as e:
        logging.error(e)
        return {"error": "something went wrong"}
