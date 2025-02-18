# data_handler_osp.py

from os import path as os_path
from zipfile import ZipFile as Zipper


class DataProcessor:
    def __init__(self, file_identifier):
        self.file_location = os_path.abspath(file_identifier)

    def load_content(self, charset="utf-8"):
        with open(self.file_location, 'r', encoding=charset) as file:
            return file.read()

    def save_content(self, information, charset="utf-8"):
        with open(self.file_location, 'w', encoding=charset) as file:
            file.write(information)

    def pack(self):
        compressed_file = os_path.splitext(self.file_location)[0] + ".zip"
        with Zipper(compressed_file, 'w') as zipped:
            zipped.write(self.file_location)

    def unpack(self):
        compressed_file = os_path.splitext(self.file_location)[0] + ".zip"
        with Zipper(compressed_file, 'r') as zipped:
            zipped.extractall()