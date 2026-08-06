from pypdf import PdfReader
import os


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF not found: {file_path}")

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text