from io import BytesIO

from minio import Minio


class MinIoConnection:
    minio_endpoint = "91.107.176.230:9000"
    minio_access_key = "6DC3MPymiCHnKrMDcM5Y"
    minio_secret_key = "9j2taXeTguvBN4owGM6OZzyIh56QpzYlcbooaZtU"
    minio_bucket_name = "docsgenerator"

    def __init__(self):
        self.minio_connection = Minio(endpoint=self.minio_endpoint,
                                      access_key=self.minio_access_key,
                                      secret_key=self.minio_secret_key,
                                      secure=False
                                      )

    def upload_file(self, file_name, doc, content_type):
        try:
            response = self.minio_connection.put_object(
                bucket_name=self.minio_bucket_name,
                object_name=file_name,
                data=BytesIO(doc),
                length=len(doc),
                content_type=content_type
            )

            return response, True
        except Exception as err:
            return str(err), None

    def download_file(self, object_name):
        try:
            response = self.minio_connection.get_object(self.minio_bucket_name, object_name=object_name)
            return response
        except Exception as err:
            return f"File download failed: {err}"


minio_client = MinIoConnection()
