import argparse
import json

from src.services.core import PrinterService
from src.utils.enum import EventType
from src.utils.logger import logger


def load_printer_name(config_path: str) -> str:
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config.get("printer_name")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Error reading config: {e}")


def controller():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type", required=True, choices=["SCAN", "COPY", "PRINT"], help="Event type"
    )
    parser.add_argument("--file_path", required=False, help="Path to the PDF file")
    parser.add_argument(
        "--pages", required=False, help='Pages to print (e.g., "1-2" or "all")'
    )
    parser.add_argument("--copies", required=False, type=int, help="Number of copies")

    args = parser.parse_args()

    printer_name = load_printer_name("config/config.json")
    if not printer_name:
        raise ValueError("'printer_name' not found in config.")

    logger.info("Starting printer service...")

    service = PrinterService(printer_name)
    event_type = EventType(args.type)

    if event_type == EventType.SCAN:
        service.print_file(event_type=EventType.SCAN)

    elif event_type == EventType.COPY:
        copies = args.copies
        if copies is None:
            logger.error("The --copies parameter for COPY was not given.")
            exit(1)
        service.print_file(copies=copies, event_type=EventType.COPY)

    elif event_type == EventType.PRINT:
        file_path = args.file_path
        pages = args.pages
        if not file_path:
            logger.error("The --file_path parameter for PRINT was not given.")
            exit(1)

        service.print_file(file_path=file_path, pages=None if pages == "all" else pages)

    logger.info("Operation completed.")
