import minio.error
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
    minio_bucket_name = "docsgenerator"

    def __init__(self):
        self.minio_connection = Minio(
            self.minio_endpoint,
            access_key=self.minio_access_key,
            secret_key=self.minio_secret_key,
            secure=False,
        )

    def upload_file(self, file_name, file_path):
        try:
            response = self.minio_connection.fput_object(
                self.minio_bucket_name, object_name=file_name, file_path=file_path
            )
            return response, True
        except minio.error as err:
            return str(err), None

    def download_file(self, object_name):
        try:
            response = self.minio_connection.get_object(self.minio_bucket_name, object_name=object_name)
            return response
        except minio.error as err:
            return f"File download failed: {err}"


minio_client = MinIoConnection()
