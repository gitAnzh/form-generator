from typing import Union

from fastapi import APIRouter
from fastapi import Query
from starlette import status
from starlette.exceptions import HTTPException

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
def user_avatar(username: str, docs: bytes = File(...)):
    return UserActions.add_image_to_user(username, docs)


@user_router.get("/get_user_detail", tags=["Users"])
def get_user(company_name: str):
    return UserActions.get_user(company_name)


@user_router.get("/main_page", tags=["Main Page"])
def main_page(searchByCompanyName: Union[str, None] = Query(default=None)):
    return UserActions.main_page_detail(searchByCompanyName)
