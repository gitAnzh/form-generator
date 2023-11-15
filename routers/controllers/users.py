from fastapi import APIRouter, UploadFile, Response, File, HTTPException, Query
from starlette import status

from routers.database.minio_connection import minio_client
from routers.users.models.auth import AuthHandler
from routers.users.models.user_model import UserActions
from routers.users.validators.user_validator import Users, UserLogin, ConfirmUser

user_router = APIRouter()
auth_handler = AuthHandler()


# Register user
@user_router.post("/register", tags=["Users"])
def register(response: Response, data: Users):
    result = UserActions(data.username).create_user(data.dict())
    if not result.get("success"):
        raise HTTPException(status_code=400, detail={"error": "UserActions name exist! try different username"})
    response.status_code = 200
    return {"message": "User registered successfully"}


# login user
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
    result = UserActions(username).add_image_to_user(filename)
    if not result:
        raise HTTPException(status_code=404, detail={"error": "no user found"})
    return {"message": "User registered successfully"}


# Get user for create form
@user_router.get("/get_user_detail", tags=["Users"])
def get_user(response: Response, company_name: str):
    result = UserActions.get_users(company_name, 1, 15)
    if not result.get("success"):
        raise HTTPException(status_code=404, detail={"error": "no user found"})
    response.status_code = 200
    del result["success"]
    return result


# Get Users for super admin
@user_router.get("/get_users", tags=["Users"])
def get_users(
        response: Response,
        page: int = Query(default=1, alias="page"),
        per_page: int = Query(default=15, alias="perPage")
):
    result = UserActions.get_users(None, page, per_page)
    if not result.get("success"):
        raise HTTPException(status_code=404, detail={"error": "no data found"})
    response.status_code = 200
    del result["success"]
    return result


# Confirm user
@user_router.post("/confirm_user", tags=["Users"])
def confirm_user(response: Response, data: ConfirmUser):
    result = UserActions(data.username).confirm_user(data.status)
    if result.get("success") is None:
        raise HTTPException(status_code=404, detail={"error": "User doesn't exist"})
    elif not result.get("success"):
        raise HTTPException(status_code=404, detail={"error": "status can't be changed for super admin"})
    response.status_code = 200
    return {"message": "User confirmed successfully"}
