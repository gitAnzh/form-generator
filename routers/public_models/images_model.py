import os
from io import BytesIO

import filetype
from fastapi import HTTPException

from routers.database.mongo_connection import MinIoConnection


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
        return f"https://form.evolvezenith.com/gallery_files/user_avatars/{path}/{name}.{file_format}"

    def set_doc_file(self, docs: list) -> list[str]:
        files = []
        for items in docs:
            if items['doc'] is not None:
                file_format = filetype.guess(items['doc']).extension
                with self.safe_open_wb(
                        f'static_files/final_files/{items["path"]}/{items["name"]}.{file_format}') as store_file:
                    store_file.write(items['doc'])
                    files.append(
                        f"https://form.evolvezenith.com/gallery_files/final_files/{items['path']}/{items['name']}.{file_format}")

        return files

    def upload_file(self, files, bucket_name):
        with MinIoConnection() as minio_client:
            try:
                file_names = []
                for file in files:
                    # Save the uploaded file to Minio
                    data = file['doc']
                    minio_client.client.put_object(
                        bucket_name=bucket_name,
                        object_name=file['name'],
                        data=BytesIO(data),
                        length=len(data),
                        content_type=file['path']
                    )
                    file_names.append(f"https://form.evolvezenith.com/form/api/v1/get/{file['name']}")
                return file_names
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Minio Error: {str(e)}")

    def get_file(self, file_name, bucket_name):
        with MinIoConnection() as minio_client:
            response = minio_client.client.get_object(
                bucket_name=bucket_name,
                object_name=file_name
            )
            return response
