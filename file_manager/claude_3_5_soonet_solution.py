# file_reader.py
from pathlib import Path
import logging


class FileReader:
    """Responsible only for reading file contents."""

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def read_file(self, file_path: Path, charset="utf-8") -> str:
        """Read and return the contents of a file."""
        try:
            with open(file_path, 'r', encoding=charset) as file:
                return file.read()
        except Exception as e:
            self.logger.error(f"Error reading file: {e}")
            raise


# file_writer.py
class FileWriter:
    """Responsible only for writing file contents."""

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def write_file(self, file_path: Path, content: str, charset="utf-8") -> None:
        """Write content to a file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding=charset) as file:
                file.write(content)
        except Exception as e:
            self.logger.error(f"Error writing file: {e}")
            raise


# file_compressor.py
from zipfile import ZipFile


class FileCompressor:
    """Responsible only for file compression operations."""

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def compress(self, file_path: Path) -> Path:
        """Compress a file to ZIP format."""
        try:
            zip_path = file_path.with_suffix('.zip')
            with ZipFile(zip_path, 'w') as zipped:
                zipped.write(file_path, file_path.name)
            return zip_path
        except Exception as e:
            self.logger.error(f"Error compressing file: {e}")
            raise


# file_decompressor.py
class FileDecompressor:
    """Responsible only for file decompression operations."""

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def decompress(self, zip_path: Path, extract_path: Path = None) -> None:
        """Extract contents from a ZIP file."""
        try:
            extract_location = extract_path or zip_path.parent
            with ZipFile(zip_path, 'r') as zipped:
                zipped.extractall(path=extract_location)
        except Exception as e:
            self.logger.error(f"Error decompressing file: {e}")
            raise


# path_handler.py
class PathHandler:
    """Responsible only for path operations and validation."""

    @staticmethod
    def validate_path(file_path: Path) -> Path:
        """Validate and return an absolute path."""
        return file_path.resolve()

    @staticmethod
    def ensure_directory_exists(path: Path) -> None:
        """Ensure the directory exists."""
        path.parent.mkdir(parents=True, exist_ok=True)
