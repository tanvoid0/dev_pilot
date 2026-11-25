import json
import os
import subprocess
import tkinter as tk
from tkinter import filedialog

import yaml

from utils.file.file_type import FileType
# from py_helper.processor.os_commander import OSCommander


class FileReaderProcessor:
    def __init__(self):
        pass

    def read(self, file_path, file_type=FileType.FILE, with_notepad=False):
        if file_path is None:
            file_path = FileReaderProcessor.select_file()
            if file_path is None:
                raise "Path has not been selected"
        if with_notepad:
            self.open_file_with_notepad(file_path)
        elif self.exists(file_path):
            if file_type == FileType.JSON:
                return self._read_json(file_path)
            if file_type == FileType.YAML:
                return self._read_yaml(file_path)
            else:
                return self._read_file(file_path)
        else:
            raise FileNotFoundError(file_path)

    @staticmethod
    def _read_file(file_path):
        try:
            with open(file_path, 'r') as file:
                return file
        except FileNotFoundError:
            print(f"File '{file_path} not found.")
        except json.JSONDecodeError as ex:
            print(f"Json decoding error: {str(ex)}")

    @staticmethod
    def _read_json(file_path: str):
        try:
            with open(file_path, 'r') as json_file:
                json_string = json_file.read()
                return json.loads(json_string)
        except FileNotFoundError as ex:
            print(f"File '{file_path} not found.")
            raise ex
        except json.JSONDecodeError as ex:
            print(f"Json decoding error: {str(ex)}")
            raise ex

    @staticmethod
    def _read_yaml(file_path):
        try:
            with open(file_path, 'r') as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        except FileNotFoundError as ex:
            print(f"File '{file_path} not found.")
            raise ex

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def open_file_with_notepad(file_name):
        # OSCommander.run(
        #     windows=lambda: subprocess.call(["notepad.exe", file_name]),
        #     linux=lambda: subprocess.call(["xdg-open", file_name]),
        #     mac=lambda: subprocess.call(["gedit", file_name]),
        # )
        pass

    @staticmethod
    def select_folder():
        print("Please select folder using the GUI window")
        root = tk.Tk()
        root.withdraw()

        return filedialog.askdirectory()

    @staticmethod
    def select_file():
        print("Please select file using the GUI window")
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename()
