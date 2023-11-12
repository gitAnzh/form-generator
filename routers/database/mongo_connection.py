from minio import Minio
from pymongo import MongoClient

from routers.config import settings

#
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
        self.forms = self.db["forms"]
        self.id = self.db["id_counter"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


class MinIoConnection:
    minio_endpoint = "91.107.176.230:9000"
    minio_access_key = "zzyAWLk6AvHd2GiK5CjC"
    minio_secret_key = "R4fMyjORMFFQJzgEMPM9XzugyYlMCZ8pJX4KvpiI"

    def __init__(self):
        self.client = Minio(
            self.minio_endpoint,
            access_key=self.minio_access_key,
            secret_key=self.minio_secret_key,
            secure=False,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
