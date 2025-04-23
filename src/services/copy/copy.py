import os
import time
from datetime import datetime
from io import BytesIO

import PIL.Image
import twain
import win32api

from src.utils.logger import logger

scanned_image = None


def scan_for_copy() -> str | None:
    """
    Scans a document and saves it as a PDF in resources/output.
    Returns the file path of the saved PDF or None if scanning failed.
    """
    global scanned_image
    output_dir = os.path.join("resources", "output")
    os.makedirs(output_dir, exist_ok=True)

    try:
        with twain.SourceManager() as sm:
            src = sm.open_source()
            if not src:
                logger.warning("No scanner source selected.")
                return None

            logger.info("Acquiring image from scanner...")
            src.request_acquire(show_ui=False, modal_ui=False)
            handle, _ = src.xfer_image_natively()
            bmp_bytes = twain.dib_to_bm_file(handle)

            img = PIL.Image.open(BytesIO(bmp_bytes), formats=["bmp"])
            width, height = img.size
            factor = 600.0 / width
            resized_img = img.resize((int(width * factor), int(height * factor)))

            scanned_image = resized_img
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_path = os.path.join(output_dir, f"scanned_{timestamp}.pdf")
            resized_img.save(pdf_path, "PDF")

            logger.info(f"Scanned image saved as PDF: {pdf_path}")
            return pdf_path

    except Exception as e:
        logger.exception(f"Failed to scan document: {e}")
        return None


def copy(copies: int):
    """
    Copies the scanned document to the printer multiple times.
    """
    file_path = scan_for_copy()

    if not file_path:
        logger.error("Copy operation aborted. Scanned file not available.")
        return

    if not os.path.exists(file_path):
        logger.error(f"Scanned file does not exist: {file_path}")
        return

    try:
        logger.info(f"Starting to print {copies} copies of {file_path}")
        for i in range(copies):
            logger.info(f"Printing copy {i + 1}/{copies}")
            win32api.ShellExecute(0, "print", file_path, None, "", 0)
            time.sleep(2)
        logger.info("All copies printed successfully.")
    except Exception as e:
        logger.exception(f"Printing failed: {e}")
