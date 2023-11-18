from passlib.context import CryptContext

from routers.database.mongo_connection import mongo_client
from routers.public_models.counter import id_counter


class UserActions:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def get_password_hash(password):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    def check_username(self):
        with mongo_client() as users_collection:
            count = users_collection.users.count_documents({"username": self.username})
            if count == 0:
                return True
            return False

    def create_user(self, user_dict: dict):
        if self.check_username():
            with mongo_client() as users_collection:
                hashed_password = UserActions.get_password_hash(user_dict.get("password"))
                user_dict.update(
                    {
                        "id": id_counter("user"),
                        "password": hashed_password,
                        "status": False,
                        "is_admin": False
                    }
                )
                users_collection.users.insert_one(user_dict)
                return {"success": True}
        return {"success": False}

    @staticmethod
    def get_users(company_name, page, per_page):
        with mongo_client() as client:
            if company_name is not None:
                data = client.users.find_one({"company_name": company_name}, {"_id": 0, "password": 0})
                if data:
                    return {"message": data, "success": True}
                return {"message": "Company not found", "success": False}
            else:
                page = page
                per = per_page
                skip = per * (page - 1)
                limit = per
                data = list(
                    client.users.aggregate(
                        [
                            {
                                '$project': {
                                    '_id': 0,
                                    'password': 0,
                                    'avatar': 0
                                },

                            },
                            {"$skip": skip},
                            {"$limit": limit}
                        ]
                    )
                )
                count = client.users.count_documents({"username": {"$ne": None}})
                return {"message": data, "count": count, "success": True}

    def add_image_to_user(self, avatar_name):
        with mongo_client() as client:
            client.users.update_one({"username": self.username}, {"$set": {"avatar": avatar_name}})
            return {"success": True}

    def confirm_user(self, status: bool):
        with mongo_client() as client:
            if self.username == "admin":
                return {"success": False}
            user = client.users.update_one({"username": self.username}, {"$set": {"status": status}})
            if user.modified_count:
                return {"success": True}
            return {"success": None}
