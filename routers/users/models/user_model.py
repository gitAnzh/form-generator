from fastapi import HTTPException
from passlib.context import CryptContext

from routers.database.mongo_connection import MongoConnection
from routers.public_models.counter import id_counter


class UserActions:
    def __init__(self, user):
        self.user = user

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
                user['id'] = id_counter("user")
                user['password'] = hashed_password
                user['status'] = False
                users_collection.users.insert_one(user)
                return {"message": "User registered successfully"}
        else:
            raise HTTPException(status_code=500, detail={"error": "UserActions name exist! try different username"})

    @staticmethod
    def get_users(company_name, page, per_page):
        with MongoConnection() as client:
            if company_name is not None:
                data = client.users.find_one({"company_name": company_name}, {"_id": 0, "password": 0})
                if data:
                    return data
                return {"message": "Company not found"}
            else:
                page = page
                per = per_page
                skip = per * (page - 1)
                limit = per
                return {"message": list(client.users.aggregate([
                    {
                        '$project': {
                            '_id': 0,
                            'password': 0,
                            'avatar': 0
                        },

                    },
                    {"$skip": skip},
                    {"$limit": limit}
                ])), "count": client.users.count_documents({"username": {"$ne": None}})}

    @staticmethod
    def add_image_to_user(username, url):
        with MongoConnection() as client:
            client.users.update_one({"username": username}, {"$set": {"avatar": url}})
            return {"message": "User registered successfully"}

    def confirm_user(self):
        with MongoConnection() as client:
            if self.user == "admin":
                return {"message": "Super admin cannot confirm!!"}
            user = client.users.update_one({"username": self.user}, {"$set": {"status": True}})
            if user.modified_count:
                return {"message": "User confirmed successfully"}
            return {"message": "User not exist"}
