import json

from src.services.core import PrinterService
from src.utils.enum import EventType
from src.utils.logger import logger


def load_printer_name(config_path: str) -> str:
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get("printer_name")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Configni o'qishda xatolik: {e}")


def get_event_type() -> EventType:
    type_input = input("Type kiriting (SCAN, COPY, PRINT): ").strip().upper()
    try:
        return EventType(type_input)
    except ValueError:
        logger.error(f"Noto'g'ri type kiritildi: {type_input}")
        exit(1)


def get_copies() -> int:
    try:
        return int(input("Nechta nusxa kerak? (copies count): "))
    except ValueError:
        logger.error("Noto'g'ri raqam kiritildi.")
        exit(1)


def get_print_details() -> tuple[str, str]:
    pages = input("Nechta sahifa chop etilsin? (pages): ").strip()
    file_path = input("Fayl manzilini kiriting (file_path): ").strip()
    return file_path, pages


def controller():
    printer_name = load_printer_name('config/config.json')
    if not printer_name:
        raise ValueError("Configda 'printer_name' topilmadi.")

    logger.info("Starting printer service...")

    service = PrinterService(printer_name)
    event_type = get_event_type()

    if event_type == EventType.SCAN:
        service.print_file(event_type=EventType.SCAN)

    elif event_type == EventType.COPY:
        copies = get_copies()
        service.print_file(copies=copies, event_type=EventType.PRINT)

    elif event_type == EventType.PRINT:
        file_path, pages = get_print_details()
        service.print_file(file_path=file_path, event_type=EventType.PRINT, pages=pages)

    logger.info("Operation completed.")
