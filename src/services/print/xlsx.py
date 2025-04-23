import os
import time

import win32com.client as win32
import win32print

from src.utils.logger import logger


def set_default_printer(printer_name: str):
    try:
        current = win32print.GetDefaultPrinter()
        win32print.SetDefaultPrinter(printer_name)
        logger.info(f"Default printer changed from '{current}' to '{printer_name}'")
        return current
    except Exception as e:
        logger.warning(f"Failed to set default printer: {e}")
        return None


def print_xlsx(file_path: str, printer_name: str = None, pages: str = None):
    """
    Prints an Excel file via COM automation.
    Optionally prints a specific range of pages (e.g., "1-2").
    """
    if not os.path.exists(file_path):
        logger.error(f"File does not exist: {file_path}")
        raise FileNotFoundError(f"Excel file not found: {file_path}")

    logger.info(
        f"Printing XLSX: {file_path} | Printer: {printer_name} | Pages: {pages}"
    )

    excel = None
    workbook = None
    previous_printer = None

    try:
        if printer_name:
            previous_printer = set_default_printer(printer_name)

        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False

        abs_path = os.path.abspath(file_path)
        workbook = excel.Workbooks.Open(abs_path)
        logger.info("Excel workbook opened successfully.")

        sheet = workbook.Worksheets(1)

        if pages:
            try:
                page_range = pages.split("-")
                from_page = int(page_range[0])
                to_page = int(page_range[1]) if len(page_range) > 1 else from_page
                sheet.PrintOut(From=from_page, To=to_page)
                logger.info(f"Printed pages {from_page} to {to_page}")
            except Exception as e:
                logger.exception(f"Invalid page range: {pages} — {e}")
                raise
        else:
            workbook.PrintOut()
            logger.info("Printed entire workbook.")

    except Exception as e:
        logger.exception(f"Failed to print Excel file: {e}")
        raise

    finally:
        if workbook:
            workbook.Close(False)
            logger.info("Excel workbook closed.")
        if excel:
            excel.Quit()
            logger.info("Excel application closed.")
        if previous_printer:
            try:
                win32print.SetDefaultPrinter(previous_printer)
                logger.info(f"Default printer restored to: {previous_printer}")
            except Exception as e:
                logger.warning(f"Could not restore previous printer: {e}")

        time.sleep(2)
