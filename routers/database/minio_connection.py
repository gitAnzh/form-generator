import minio.error
from minio import Minio

from routers.config import settings


class MinIoConnection:

    def __init__(self):
        self.minio_connection = Minio(
            f'{settings.MINIO_HOST}:{settings.MINIO_PORT}',
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.SECRET_KEY,
            secure=False,
        )

    def upload_file(self, file_name, file_path):
        try:
            response = self.minio_connection.fput_object(
                settings.MINIO_BUCKET_NAME, object_name=file_name, file_path=file_path
            )
            return response, True
        except minio.error as err:
            return str(err), None

    def download_file(self, object_name):
        try:
            response = self.minio_connection.get_object(settings.MINIO_BUCKET_NAME, object_name=object_name)
            return response
        except minio.error as err:
            return f"File download failed: {err}"


minio_client = MinIoConnection()
