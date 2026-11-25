import json
import os
import shutil

import yaml

from utils.file.file_type import FileType


class FileWriterProcessor:

    def __init__(self):
        pass

    def write(self, file_path: str, file_data=None, file_type=FileType.FILE):
        if file_type == FileType.JSON:
            self._write_json(file_path, file_data)
        elif file_type == FileType.YAML:
            self._write_yaml(file_path, file_data)
        else:
            self._write_file(file_path, file_data)

    @staticmethod
    def create_folder_if_does_not_exist(folder_path):
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

    def create_file_with_folder(self, folder_path, file_path, file_data, file_type):
        self.create_folder_if_does_not_exist(folder_path)
        file_path = os.path.join(folder_path, file_path)
        self.write(file_path, file_data, file_type)

    @staticmethod
    def _write_file(file_name, file_data=None):
        with open(file_name, "w") as f:
            f.write("" if file_data is None else file_data)

    @staticmethod
    def _write_json(file_path, file):
        try:
            with open(file_path, 'w') as json_file:
                json_file.write(json.dumps(file, indent=2))
        except FileNotFoundError:
            print(f"File '{file_path} not found.")

    @staticmethod
    def _write_yaml(file_name, data):
        if not isinstance(data, dict):
            data = yaml.safe_load(data)
        with open(file_name, 'w') as file:
            yaml.dump(data, file)

    @staticmethod
    def copy_file(source_file, destination_file):
        try:
            shutil.copy(source_file, destination_file)
            # subprocess.run(["copy", source_file, destination_file], shell=True)
        except Exception as ex:
            print("Error copying file")
            raise ex
