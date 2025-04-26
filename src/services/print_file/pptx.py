import os
import time

import win32com.client as win32

from src.utils.logger import logger


def print_pptx(file_path: str, printer_name: str = None):
    """
    Prints a PowerPoint presentation using Microsoft PowerPoint COM automation.
    """
    if not os.path.exists(file_path):
        logger.error(f"File does not exist: {file_path}")
        raise FileNotFoundError(f"File does not exist: {file_path}")

    logger.info(f"Printing PPTX: {file_path} | Printer: {printer_name}")

    powerpoint = None
    presentation = None

    try:
        powerpoint = win32.Dispatch("PowerPoint.Application")
        powerpoint.Visible = False

        abs_path = os.path.abspath(file_path)
        presentation = powerpoint.Presentations.Open(abs_path, WithWindow=False)
        logger.info("PowerPoint presentation opened successfully.")

        presentation.PrintOut()
        logger.info("Presentation sent to printer.")

    except Exception as e:
        logger.exception(f"Failed to print PowerPoint file: {e}")
        raise

    finally:
        if presentation:
            presentation.Close()
            logger.info("Presentation closed.")
        if powerpoint:
            powerpoint.Quit()
            logger.info("PowerPoint application closed.")

        time.sleep(2)
