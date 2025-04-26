import win32print

from src.exceptions.exception import UnsupportedFileTypeError
from src.services.copy.copy import copy
from src.services.print_file.core import print_file
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
                scan(save_dir="resources/output/scans")
                logger.info("Scanning completed.")

            elif event_type == EventType.COPY:
                copy(copies)
                logger.info(f"Copied document {copies} times.")

            elif event_type == EventType.PRINT:
                print_file(file_path, self.printer_name, pages)
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
