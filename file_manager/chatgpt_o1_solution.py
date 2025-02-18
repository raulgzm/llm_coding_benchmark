import os
import zipfile
from typing import Optional

class FileHandler:
    """
    A class responsible for reading and writing text data to a file.
    """

    def __init__(self, file_path: str):
        """
        :param file_path: The path to the file to be read or written.
        """
        self.file_path = os.path.abspath(file_path)

    def load_content(self, charset: str = "utf-8") -> str:
        """
        Reads text content from the file.

        :param charset: The character encoding to use for reading.
        :return: The file contents as a string.
        :raises FileNotFoundError: If the file does not exist.
        :raises OSError: If there's an error opening or reading the file.
        """
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        with open(self.file_path, mode='r', encoding=charset) as file:
            return file.read()

    def save_content(self, content: str, charset: str = "utf-8") -> None:
        """
        Writes (or overwrites) text content to the file.

        :param content: The text content to write.
        :param charset: The character encoding to use for writing.
        :raises OSError: If there's an error opening or writing to the file.
        """
        with open(self.file_path, mode='w', encoding=charset) as file:
            file.write(content)


class FileArchiver:
    """
    A class responsible for compressing and decompressing a single file into a .zip archive.
    """

    def __init__(self, file_path: str):
        """
        :param file_path: The path to the file that will be compressed/uncompressed.
        """
        self.file_path = os.path.abspath(file_path)

    def pack(self, compression: int = zipfile.ZIP_DEFLATED) -> str:
        """
        Compresses the file into a .zip archive in the same directory.

        :param compression: Compression type (e.g., zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED).
        :return: The path to the created .zip file.
        :raises FileNotFoundError: If the source file does not exist.
        :raises OSError: If there's an error creating or writing to the .zip file.
        """
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        zip_path = os.path.splitext(self.file_path)[0] + ".zip"
        with zipfile.ZipFile(zip_path, mode='w', compression=compression) as zipped:
            zipped.write(
                self.file_path,
                arcname=os.path.basename(self.file_path)
            )

        return zip_path

    def unpack(self, extract_path: Optional[str] = None) -> None:
        """
        Extracts the contents from the corresponding .zip file to the specified directory.

        :param extract_path: The directory where to extract the files (default: current directory).
        :raises FileNotFoundError: If the .zip archive doesn't exist.
        :raises zipfile.BadZipFile: If the .zip archive is invalid or corrupt.
        """
        zip_path = os.path.splitext(self.file_path)[0] + ".zip"
        if not os.path.isfile(zip_path):
            raise FileNotFoundError(f"Zip archive not found for {self.file_path}")

        with zipfile.ZipFile(zip_path, mode='r') as zipped:
            zipped.extractall(path=extract_path)
