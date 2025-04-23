import os

import win32print

from src.exceptions.exception import UnsupportedFileTypeError
from src.services.copy.copy import copy
from src.services.print.docx import print_docx
from src.services.print.pdf import print_pdf
from src.services.print.pptx import print_pptx
from src.services.print.xlsx import print_xlsx
from src.services.scan.scan import scan
from src.utils.enum import EventType
from src.utils.logger import logger


class PrinterService:
    def __init__(self, printer: str = None):
        self.printer_name = printer
        try:
            self.set_default_printer(printer)
        except Exception as e:
            logger.error(f"Failed to set default printer: {e}")
            raise

    @staticmethod
    def set_default_printer(printer: str):
        if printer:
            try:
                win32print.SetDefaultPrinter(printer)
                logger.info(f"Default printer set to: {printer}")
            except Exception as e:
                logger.error(f"Could not set default printer: {e}")
                raise

    def print_file(
            self,
            file_path: str = None,
            pages: str = None,
            copies: int = 1,
            event_type: EventType = EventType.PRINT,
    ):
        try:
            if event_type == EventType.SCAN:
                scan()
                logger.info("Scanning completed.")

            elif event_type == EventType.COPY:
                copy(copies)
                logger.info(f"Copied document {copies} times.")

            elif event_type == EventType.PRINT:
                logger.info(
                    f"Initiating print job for: {file_path} with {pages or 'all'} pages"
                )

                if not os.path.exists(file_path):
                    logger.error(f"File not found: {file_path}")
                    raise FileNotFoundError(f"The file '{file_path}' does not exist.")

                ext = os.path.splitext(file_path)[1].lower()
                self.set_default_printer(self.printer_name)

                if ext == ".pdf":
                    print_pdf(file_path, pages)
                elif ext in (".doc", ".docx"):
                    print_docx(file_path, self.printer_name, pages)
                elif ext in (".xls", ".xlsx"):
                    print_xlsx(file_path, self.printer_name, pages)
                elif ext in (".ppt", ".pptx"):
                    print_pptx(file_path, self.printer_name)
                else:
                    raise UnsupportedFileTypeError(f"Unsupported file type: {ext}")

                logger.info("Printing completed successfully.")
        except FileNotFoundError as e:
            logger.exception(f"File not found error. {e}")
            raise
        except UnsupportedFileTypeError(f"Unsupported file type.") as e:
            logger.exception(f"Unsupported file type. {e}")
            raise
        except Exception as e:
            logger.exception(
                f"Unexpected error during {event_type.value.lower()} operation: {e}"
            )
            raise


if __name__ == "__main__":
    try:
        printer_name = "Canon iR2006/2206 UFRII LT"
        # printer_name = "Canon iR2006/2206"
        file_path = r"D:\PythonJob\Ksero\resources\test.pptx"

        logger.info("Starting printer service...")
        service = PrinterService(printer_name)
        # service.print_file(file_path=file_path, event_type=EventType.PRINT)
        service.print_file(event_type=EventType.SCAN)
        logger.info("Operation completed.")
    except Exception as e:
        logger.critical(f"Unhandled exception in main: {e}")
