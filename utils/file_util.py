import json
import os

from pathlib import Path

class FileUtil:
    encoding = 'utf-8'

    @staticmethod
    def save(path: str, content: str, file_type=None):
        try:
            file_path = Path(path)
            if file_type is None:
                file_path.write_text(content, encoding=FileUtil.encoding)
            elif file_type == 'json':
                with open(path, 'w') as f:
                    json.dump(content, f, indent=2)
            else:
                raise TypeError('file_type must be "json" or None')
        except Exception as e:
            print(f"An error occurred saving {path}: {e}")


    @staticmethod
    def read(path: str, file_type: str=None, graceful=True):
        file_path = Path(path)
        if not file_path.exists():
            if graceful:
                return None
            raise FileNotFoundError(f"File {path} not found.")
        if file_type is None:
            return file_path.read_text(encoding=FileUtil.encoding)
        elif file_type is 'json':
            return json.loads(file_path.read_text(encoding=FileUtil.encoding))
        else:
            raise NotImplementedError(f'invalid file type - {file_type}')

    @staticmethod
    def create_if_not_exists(path):
        """
          Creates the file at the specified path if it doesn't exist.
          Also creates the directory if it doesn't exist.
          """
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        if not os.path.exists(path):
            FileUtil.write_json_file(path, {})

    @staticmethod
    def read_json_file(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError as ex:
            print("File not found")
            raise ex
        except json.JSONDecodeError as ex:
            print("Invalid JSON Format")
            raise ex

    @staticmethod
    def write_json_file(file_path, data):
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as ex:
            print(f"An error occurred: {ex}")


