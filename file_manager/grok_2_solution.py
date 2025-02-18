from os import path as os_path
from zipfile import ZipFile as Zipper

class FileReader:
    def __init__(self, file_identifier):
        self.file_location = os_path.abspath(file_identifier)

    def read_content(self, charset="utf-8"):
        with open(self.file_location, 'r', encoding=charset) as file:
            return file.read()

    def write_content(self, information, charset="utf-8"):
        with open(self.file_location, 'w', encoding=charset) as file:
            file.write(information)


class FileCompressor:
    def __init__(self, file_identifier):
        self.file_location = os_path.abspath(file_identifier)

    def compress(self):
        zip_name = os_path.splitext(self.file_location)[0] + "_archive.zip"
        with Zipper(zip_name, 'w') as zipped:
            zipped.write(self.file_location)

    def decompress(self, destination=None):
        if destination is None:
            destination = os_path.dirname(self.file_location)
        zip_name = os_path.splitext(self.file_location)[0] + "_archive.zip"
        with Zipper(zip_name, 'r') as zipped:
            zipped.extractall(path=destination)