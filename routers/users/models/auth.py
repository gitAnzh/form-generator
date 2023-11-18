from datetime import datetime, timedelta
from typing import Union, Any, Optional

import jwt
from fastapi import HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from jwt import exceptions as jwt_exceptions
from passlib.context import CryptContext

from routers.database.mongo_connection import mongo_client


class AuthHandler:
    SECRET_KEY = "esi"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    # Verify password
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str):
        with mongo_client() as users_collection:
            user = users_collection.users.find_one({"username": username})
            if user and AuthHandler.verify_password(self, password, user["password"]):
                return user

    def decode_access_token(self, token: str) -> Union[Optional[bool], Any]:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
        except jwt_exceptions.ExpiredSignatureError:
            return None

        except jwt_exceptions.InvalidSignatureError:
            return False

        except jwt_exceptions.InvalidAlgorithmError:
            return False

        except jwt_exceptions.InvalidTokenError:
            return False

        else:
            return payload if payload.get("scope") == "access" and not payload.get("expired") else False

    def decode_refresh_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
        except jwt_exceptions.ExpiredSignatureError:
            return None
        except jwt_exceptions.InvalidSignatureError:
            return False
        except jwt_exceptions.InvalidAlgorithmError:
            return False
        except jwt_exceptions.InvalidTokenError:
            return False
        else:
            return payload if payload.get("scope") == "refresh" else False

    def encode_access_token(self, sud_dict: dict) -> str:
        pay_load = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=20),
            'iat': datetime.utcnow(),
            'sub': sud_dict,
            'scope': 'access',
            "expired": False
        }
        return jwt.encode(pay_load, self.SECRET_KEY, algorithm='HS256')

    def encode_refresh_token(self, sud_dict: dict) -> str:
        pay_load = {
            'exp': datetime.utcnow() + timedelta(days=20),
            'iat': datetime.utcnow(),
            'sub': sud_dict,
            'scope': 'refresh'
        }
        return jwt.encode(pay_load, self.SECRET_KEY, algorithm='HS256')

    def check_current_user_tokens(self, access: str = Header(...), refresh: str = Header(...)):
        access = access.replace(" ", "")
        refresh = refresh.replace(" ", "")
        access_tok_payload = AuthHandler.decode_access_token(self, access)
        refresh_tok_payload = AuthHandler.decode_refresh_token(self, refresh)

        # for invalid token
        if access_tok_payload is False:
            raise HTTPException(status_code=401, detail={"error": "مجددا وارد شوید", "redirect": "login"})

        if access_tok_payload:
            user_data = access_tok_payload.get("sub")
            tokens = {
                "access_token_payload": access_tok_payload,
                "refresh_token_payload": refresh_tok_payload,
                "access_token": access,
                "refresh_token": refresh,
            }
            return user_data, tokens

        elif access_tok_payload is None and refresh_tok_payload:
            user_data = refresh_tok_payload.get("sub")
            new_access_token = AuthHandler.encode_access_token(self, user_data)
            tokens = {
                "access_token_payload": access_tok_payload,
                "refresh_token_payload": refresh_tok_payload,
                "access_token": new_access_token,
                "refresh_token": refresh,
            }
            return user_data, tokens

        else:
            raise HTTPException(status_code=401, detail={"error": "login again", "redirect": "login"})
