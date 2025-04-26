import os
import time

import win32com.client as win32

from src.utils.logger import logger


def print_docx(file_path: str, printer_name: str = None, pages: str = None):
    """
    Prints a Word document using Microsoft Word COM automation.
    """
    if not os.path.exists(file_path):
        logger.error(f"File does not exist: {file_path}")
        raise FileNotFoundError(f"File does not exist: {file_path}")

    logger.info(
        f"Printing DOCX: {file_path} | Printer: {printer_name} | Pages: {pages}"
    )

    word = None
    doc = None

    try:
        word = win32.Dispatch("Word.Application")
        word.Visible = False

        doc = word.Documents.Open(os.path.abspath(file_path))
        logger.info("Word document opened successfully.")

        if printer_name:
            word.ActivePrinter = printer_name
            logger.info(f"Printer set to: {printer_name}")

        if pages:
            logger.info(f"Printing specific pages: {pages}")
            doc.PrintOut(Pages=pages)
        else:
            logger.info("Printing all pages.")
            doc.PrintOut()

        logger.info("Document sent to printer.")

    except Exception as e:
        logger.exception(f"Failed to print Word document: {e}")
        raise

    finally:
        if doc:
            doc.Close(False)
            logger.info("Word document closed.")
        if word:
            word.Quit()
            logger.info("Word application closed.")

        time.sleep(2)
