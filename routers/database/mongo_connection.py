from pymongo import MongoClient

from routers.config import settings


# class MongoConnection:
#     client = None
#
#     def __init__(self):
#         self.client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT,
#                                   username=settings.MONGO_USER,
#                                   password=settings.MONGO_PASS) if not self.client else self.client
#         self.db = self.client['form-generator']
#         self.users = self.db["users"]
#         self.forms = self.db["forms"]
#         self.id = self.db["id_counter"]
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.client.close()


class MongoConnection:
    client = None

    def __init__(self):
        self.client = MongoClient(settings.MONGO_CONTAINERNAME,
                                  username=settings.MONGO_USER,
                                  password=settings.MONGO_PASS) if not self.client else self.client
        self.db = self.client['form-generator']
        self.users = self.db["users"]
        self.id = self.db["id_counter"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()