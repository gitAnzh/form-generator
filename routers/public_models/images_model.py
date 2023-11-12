from io import BytesIO

from fastapi import HTTPException

from routers.database.mongo_connection import MinIoConnection


class Images:
    @staticmethod
    def upload_file(files):
        with MinIoConnection() as client:
            try:
                file_names = []
                for file in files:
                    # Save the uploaded file to Minio
                    data = file['doc']
                    client.minio_connection.put_object(
                        bucket_name=client.minio_bucket_name,
                        object_name=file['name'],
                        data=BytesIO(data),
                        length=len(data),
                        content_type=file['path']
                    )
                    file_names.append(f"https://form.evolvezenith.com/form/api/v1/get/{file['name']}")
                return file_names
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Minio Error: {str(e)}")

    @staticmethod
    def get_file(file_name):
        with MinIoConnection() as client:
            response = client.minio_connection.get_object(
                bucket_name=client.minio_bucket_name,
                object_name=file_name
            )
            return response
