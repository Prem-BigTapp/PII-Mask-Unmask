# Directory: PIIAgenticSystem/utils
# File: file_handler.py

import os
import PyPDF2
from typing import Optional

class FileHandler:
    def extract_text_from_pdf(self, file_path: str) -> Optional[str]:
        try:
            text = ""
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() or ""
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None

    def read_text_file(self, file_path: str) -> Optional[str]:
        try:
            with open(file_path, "r") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading text file: {e}")
            return None

    def get_text_from_file(self, file_path: str) -> Optional[str]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".txt":
            return self.read_text_file(file_path)
        elif ext == ".pdf":
            return self.extract_text_from_pdf(file_path)
        print("Unsupported file format. Please provide a .txt or .pdf file.")
        return None