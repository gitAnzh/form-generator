import os

import filetype


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
