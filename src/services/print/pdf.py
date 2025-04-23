import os
import time

import win32api
from PyPDF2 import PdfReader, PdfWriter

from src.utils.logger import logger


def extract_pages(input_pdf: str, output_pdf: str, pages: str):
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        logger.info(f"Extracting pages: {pages} from {input_pdf}")
        for part in pages.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                for i in range(start, end + 1):
                    writer.add_page(reader.pages[i - 1])
            else:
                writer.add_page(reader.pages[int(part) - 1])

        with open(output_pdf, "wb") as f:
            writer.write(f)

        logger.info(f"Pages extracted to: {output_pdf}")
    except Exception as e:
        logger.exception(f"Failed to extract pages from PDF: {e}")
        raise


def print_pdf(file_path: str, pages: str = None):
    if not os.path.exists(file_path):
        logger.error(f"PDF file not found: {file_path}")
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    logger.info(f"Preparing to print PDF: {file_path} | Pages: {pages}")
    extracted_path = None

    try:
        if pages:
            extracted_path = "temp_extracted.pdf"
            extract_pages(file_path, extracted_path, pages)
            file_path = extracted_path

        logger.info(f"Sending PDF to printer: {file_path}")
        win32api.ShellExecute(0, "print", file_path, None, "", 0)
        logger.info("Print command sent to default printer.")

        time.sleep(2)

    except Exception as e:
        logger.exception(f"Failed to print PDF: {e}")
        raise

    finally:
        if extracted_path and os.path.exists(extracted_path):
            os.remove(extracted_path)
            logger.info(f"Temporary file removed: {extracted_path}")
