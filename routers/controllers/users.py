from fastapi import APIRouter, UploadFile, Response
from starlette import status
from starlette.exceptions import HTTPException

from routers.database.mongo_connection import minio_client
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
        "is_admin": user.get("is_admin")
    }
    access_token = auth_handler.encode_access_token(sub_dict)
    refresh_token = auth_handler.encode_refresh_token(sub_dict)
    return {"access_token": access_token, "refresh_token": refresh_token, "message": "login successfully"}


# Add user avatar
@user_router.post("/user_avatar", tags=["Users"])
def user_avatar(fastapi_response: Response, username: str, docs: UploadFile = File(...)):
    filename = f"{username}.{docs.filename.split('.')[-1]}"
    response, result = minio_client.upload_file(file_name=filename, file_path=docs.file.fileno())
    if not result:
        raise HTTPException(status_code=400, detail={"error": response or "something went wrong"})
    fastapi_response.status_code = 200
    return UserActions.add_image_to_user(username, filename)


@user_router.get("/get_user_detail", tags=["Users"])
def get_user(response: Response, company_name: str):
    data, result = UserActions.get_users(company_name, 1, 15)
    if not result:
        raise HTTPException(status_code=404, detail={"error": "no user found"})
    response.status_code = 200
    return data


@user_router.get("/get_users", tags=["Users"])
def get_users(response: Response, page: int, perPage: int):
    data, result = UserActions.get_users(None, page, perPage)
    if not result:
        raise HTTPException(status_code=404, detail={"error": "no data found"})
    response.status_code = 200
    return data


# # Register user
@user_router.post("/confirm_user", tags=["Users"])
def confirm_user(username: str):
    user_ins = UserActions(username)
    return user_ins.confirm_user()
