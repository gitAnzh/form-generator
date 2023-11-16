import minio.error
from minio import Minio

from routers.config import settings


class MinIoConnection:
    minio_endpoint = "91.107.176.230:9000"
    minio_access_key = "zzyAWLk6AvHd2GiK5CjC"
    minio_secret_key = "R4fMyjORMFFQJzgEMPM9XzugyYlMCZ8pJX4KvpiI"
    minio_bucket_name = "docsgenerator"

    def __init__(self):
        self.minio_connection = Minio(endpoint=self.minio_endpoint,
                                      access_key="6DC3MPymiCHnKrMDcM5Y",
                                      secret_key="9j2taXeTguvBN4owGM6OZzyIh56QpzYlcbooaZtU",
                                      secure=False
                                      )

    def upload_file(self, file_name, file_path):
        try:
            a = self.minio_connection.bucket_exists(settings.MINIO_BUCKET_NAME)
            response = self.minio_connection.fput_object(
                settings.MINIO_BUCKET_NAME, object_name=file_name, file_path=file_path
            )
            return response, True
        except Exception as err:
            return str(err), None

    def download_file(self, object_name):
        try:
            response = self.minio_connection.get_object(settings.MINIO_BUCKET_NAME, object_name=object_name)
            return response
        except minio.error as err:
            return f"File download failed: {err}"


minio_client = MinIoConnection()
