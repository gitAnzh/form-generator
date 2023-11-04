import re

from fastapi import HTTPException
from passlib.context import CryptContext

from routers.database.mongo_connection import MongoConnection
from routers.public_models.images_model import Images


class UserActions:
    def __init__(self, user):
        self.user = user

    @staticmethod
    def id_counter(request_type):
        with MongoConnection() as client:
            id = client.id.find_one({"type": request_type})
            if id:
                client.id.update_one({"type": request_type}, {"$inc": {"counter": 1}})
                return id.get("counter")
            else:
                client.id.insert_one({"type": request_type, "counter": 1})
                return 1

    @staticmethod
    def get_password_hash(password):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    @staticmethod
    def check_username(user):
        with MongoConnection() as users_collection:
            count = users_collection.users.count_documents({"username": user.username})
            if count == 0:
                return True
            return False

    def create_user(self):
        if UserActions.check_username(self.user):
            with MongoConnection() as users_collection:
                hashed_password = UserActions.get_password_hash(self.user.password)
                user = dict(self.user)
                user['id'] = UserActions.id_counter("user")
                user['password'] = hashed_password
                user['status'] = False
                users_collection.users.insert_one(user)
                return {"message": "User registered successfully"}
        else:
            raise HTTPException(status_code=500, detail={"error": "UserActions name exist! try different username"})

    @staticmethod
    def add_image_to_user(username, docs):
        images = Images()
        url = images.set_avatar_file(username, username, docs)
        with MongoConnection() as client:
            client.users.update_one({"username": username}, {"$set": {"avatar": url}})
            return {"message": "User registered successfully"}

    @staticmethod
    def get_user(company_name):
        with MongoConnection() as client:
            return client.users.find_one({"company_name": company_name}, {"_id": 0, "password": 0})

    @staticmethod
    def main_page_detail(searchByCompanyName):
        with MongoConnection() as client:
            match = {}
            if searchByCompanyName:
                match = {"company_name": {
                    '$regex': re.compile(rf"{searchByCompanyName}(?i)")
                }}
            return list(client.users.aggregate([
                {
                    '$match': match
                }, {
                    '$project': {
                        'company_name': 1,
                        'avatar': 1,
                        '_id': 0
                    }
                }
            ]))

