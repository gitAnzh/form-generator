import os

import filetype
from fastapi import HTTPException
from passlib.context import CryptContext

from routers.database.mongo_connection import MongoConnection


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


class Images:
    @staticmethod
    def safe_open_wb(path):
        """
        Open "path" for writing, creating any parent directories as needed.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)

        return open(path, 'wb')

    def set_avatar_file(self, path: str, name: str, doc: bytes) -> str:
        """
        used for uploading files
        """
        file_format = filetype.guess(doc).extension
        with self.safe_open_wb(f'static_files/user_avatars/{path}/{name}.{file_format}') as store_file:
            store_file.write(doc)
        return f"http://65.108.246.44:85/gallery_files/user_avatars/{path}/{name}.{file_format}"

    def set_final_file(self, docs: list) -> list[str]:
        files = []
        for items in docs:
            file_format = filetype.guess(items['doc']).extension
            with self.safe_open_wb(
                    f'static_files/final_files/{items["path"]}/{items["name"]}.{file_format}') as store_file:
                store_file.write(items['doc'])
                files.append(
                    f"https://localhost:8099/gallery_files/user_avatars/{items['path']}/{items['name']}.{file_format}")
        return files
