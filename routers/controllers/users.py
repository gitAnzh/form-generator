from typing import Union

from fastapi import APIRouter, UploadFile
from fastapi import Query
from starlette import status
from starlette.exceptions import HTTPException

from routers.public_models.images_model import Images
from routers.public_models.main_page import main_page_detail
from routers.users.models.auth import AuthHandler
from routers.users.models.user_model import *
from routers.users.validators.user_validator import *

user_router = APIRouter()
auth_handler = AuthHandler()


# Register user
@user_router.post("/register", tags=["Users"])
def register(data: Users):
    user_instance = UserActions(data)
    return user_instance.create_user()


@user_router.post("/login", tags=["Users"])
def login(login_data: UserLogin):
    user = auth_handler.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    sub_dict = {
        "staff_id": user.get('id'),
        "username": user.get('username'),
        "company_name": user.get('company_name'),
    }
    access_token = auth_handler.encode_access_token(sub_dict)
    refresh_token = auth_handler.encode_refresh_token(sub_dict)
    return {"access_token": access_token, "refresh_token": refresh_token, "message": "login successfully"}


#
# # Register user
@user_router.post("/user_avatar", tags=["Users"])
async def user_avatar(username: str, docs: UploadFile = File(...)):
    docs_data = [{"name": username, "path": docs.content_type, "doc": await docs.read()}]
    response = Images.upload_file(docs_data)
    return UserActions.add_image_to_user(username, response[0])


@user_router.get("/get_user_detail", tags=["Users"])
def get_user(company_name: str):
    return UserActions.get_user(company_name)


@user_router.get("/main_page", tags=["Main Page"])
def main_page(search: Union[str, None] = Query(default=None, alias="searchByCompanyName")):
    return main_page_detail(search)
