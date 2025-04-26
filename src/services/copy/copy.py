import os
import time

import win32api

from src.services.scan.scan import scan
from src.utils.logger import logger


def copy(copies: int):
    """
    Copies the scanned document to the printer multiple times.
    """
    file_path = scan(save_dir="resources/output/scans")

    if not file_path:
        logger.error("Copy operation aborted. Scanned file not available.")
        return

    if not os.path.exists(file_path):
        logger.error(f"Scanned file does not exist: {file_path}")
        return

    try:
        logger.info(f"Starting to print_file {copies} copies of {file_path}")
        for i in range(copies):
            logger.info(f"Printing copy {i + 1}/{copies}")
            win32api.ShellExecute(0, "print", file_path, None, "", 0)
            time.sleep(2)
        logger.info("All copies printed successfully.")
    except Exception as e:
        logger.exception(f"Printing failed: {e}")
