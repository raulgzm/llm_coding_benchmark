from os import path as os_path
from zipfile import ZipFile as Zipper
from typing import Optional, Protocol

# Define an interface for compression
class Compressor(Protocol):
    def compress(self, source_path: str, destination_path: str) -> bool:
        ...

    def decompress(self, source_path: str, destination_dir: str) -> bool:
        ...

# Implement a ZipCompressor
class ZipCompressor:
    def compress(self, source_path: str, destination_path: str) -> bool:
        try:
            with Zipper(destination_path, 'w') as zipped:
                zipped.write(source_path)
            return True
        except IOError as e:
            print(f"Error compressing file: {e}")
            return False

    def decompress(self, source_path: str, destination_dir: str) -> bool:
        try:
            with Zipper(source_path, 'r') as zipped:
                zipped.extractall(destination_dir)
            return True
        except (IOError, FileNotFoundError) as e:
            print(f"Error decompressing file: {e}")
            return False

# FileHandler class for file operations
class FileHandler:
    def __init__(self, file_path: str):
        self._file_path = os_path.abspath(file_path)

    def load_content(self, charset: str = "utf-8") -> Optional[str]:
        try:
            with open(self._file_path, 'r', encoding=charset) as file:
                return file.read()
        except (IOError, FileNotFoundError) as e:
            print(f"Error loading file: {e}")
            return None

    def save_content(self, information: str, charset: str = "utf-8") -> bool:
        try:
            with open(self._file_path, 'w', encoding=charset) as file:
                file.write(information)
            return True
        except IOError as e:
            print(f"Error saving file: {e}")
            return False

# DataProcessor class that uses FileHandler and Compressor
class DataProcessor:
    def __init__(self, file_path: str, compressor: Compressor):
        self._file_handler = FileHandler(file_path)
        self._compressor = compressor

    def load_content(self, charset: str = "utf-8") -> Optional[str]:
        return self._file_handler.load_content(charset)

    def save_content(self, information: str, charset: str = "utf-8") -> bool:
        return self._file_handler.save_content(information, charset)

    def compress(self, destination_path: str) -> bool:
        return self._compressor.compress(self._file_handler._file_path, destination_path)

    def decompress(self, destination_dir: str) -> bool:
        return self._compressor.decompress(self._file_handler._file_path, destination_dir)