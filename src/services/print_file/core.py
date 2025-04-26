import os

from src.exceptions.exception import UnsupportedFileTypeError
from src.services.print_file.docx import print_docx
from src.services.print_file.pdf import print_pdf
from src.services.print_file.pptx import print_pptx
from src.services.print_file.xlsx import print_xlsx
from src.utils.logger import logger


def print_file(file_path: str, printer_name: str = None, pages: str = None):
    logger.info(
        f"Initiating print job for: {file_path} with {pages or 'all'} pages"
    )

    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return print_pdf(file_path, pages)
    elif ext in (".doc", ".docx"):
        return print_docx(file_path, printer_name, pages)
    elif ext in (".xls", ".xlsx"):
        return print_xlsx(file_path, printer_name, pages)
    elif ext in (".ppt", ".pptx"):
        return print_pptx(file_path, printer_name)
    else:
        raise UnsupportedFileTypeError(f"Unsupported file type: {ext}")
