import os
import logging
from abc import ABC, abstractmethod
from zipfile import ZipFile

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# ---------------- SEPARATING RESPONSIBILITIES ---------------- #

class FileHandler:
    """Handles file reading and writing."""

    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)

    def load_content(self, charset="utf-8"):
        """Loads file content."""
        if not os.path.exists(self.file_path):
            logging.error(f"File not found: {self.file_path}")
            return None
        try:
            with open(self.file_path, 'r', encoding=charset) as file:
                return file.read()
        except Exception as e:
            logging.error(f"Error reading {self.file_path}: {e}")
            return None

    def save_content(self, content, charset="utf-8"):
        """Saves content to a file."""
        try:
            with open(self.file_path, 'w', encoding=charset) as file:
                file.write(content)
            logging.info(f"File saved: {self.file_path}")
        except Exception as e:
            logging.error(f"Error saving {self.file_path}: {e}")


# ---------------- APPLYING DEPENDENCY INVERSION ---------------- #

class Compressor(ABC):
    """Abstract class for compression strategies."""

    @abstractmethod
    def compress(self, file_path):
        pass

    @abstractmethod
    def extract(self, compressed_path, extract_to):
        pass


class ZipCompressor(Compressor):
    """ZIP file compression strategy."""

    def compress(self, file_path):
        """Compresses the file into a ZIP archive."""
        if not os.path.exists(file_path):
            logging.error(f"Cannot compress. File does not exist: {file_path}")
            return None

        compressed_file = f"{file_path}.zip"
        try:
            with ZipFile(compressed_file, 'w') as zipped:
                zipped.write(file_path, os.path.basename(file_path))
            logging.info(f"File compressed: {compressed_file}")
            return compressed_file
        except Exception as e:
            logging.error(f"Error compressing {file_path}: {e}")
            return None

    def extract(self, compressed_path, extract_to):
        """Extracts the ZIP archive."""
        if not os.path.exists(compressed_path):
            logging.error(f"ZIP file not found: {compressed_path}")
            return

        try:
            with ZipFile(compressed_path, 'r') as zipped:
                zipped.extractall(extract_to)
            logging.info(f"Extracted {compressed_path} to {extract_to}")
        except Exception as e:
            logging.error(f"Error extracting {compressed_path}: {e}")


# ---------------- HIGH-LEVEL CLASS ---------------- #

class DataProcessor:
    """High-level class that manages file operations with dependency injection."""

    def __init__(self, file_handler: FileHandler, compressor: Compressor):
        self.file_handler = file_handler
        self.compressor = compressor

    def process(self, content):
        """Saves content and compresses it."""
        self.file_handler.save_content(content)
        return self.compressor.compress(self.file_handler.file_path)

    def restore(self, extract_to=None):
        """Extracts the compressed file."""
        compressed_file = f"{self.file_handler.file_path}.zip"
        self.compressor.extract(compressed_file, extract_to or os.path.dirname(self.file_handler.file_path))

