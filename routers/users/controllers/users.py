from fastapi import APIRouter
from starlette import status

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
        "company_name": user.get('company_name')
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
def get_user(username: str):
    return UserActions.get_user(username)

#
# @user_router.post("/user_final", tags=["Users"])
# def user_final(refferal_number: str, docs1: bytes = File(...), docs2: bytes = File(...), docs3: bytes = File(...),
#                docs4: bytes = File(...), docs5: bytes = File(...), docs6: bytes = File(...)):
#     image = Images()
#     docs = [{"name": f'{refferal_number}-1', "path": refferal_number, "doc": docs1},
#             {"name": f'{refferal_number}-2', "path": refferal_number, "doc": docs2},
#             {"name": f'{refferal_number}-3', "path": refferal_number, "doc": docs3},
#             {"name": f'{refferal_number}-4', "path": refferal_number, "doc": docs4},
#             {"name": f'{refferal_number}-5', "path": refferal_number, "doc": docs5},
#             {"name": f'{refferal_number}-6', "path": refferal_number, "doc": docs6}
#             ]
#     return image.set_final_file(docs)
