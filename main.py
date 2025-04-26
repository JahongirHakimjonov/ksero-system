from src.controller.core import controller
from src.utils.logger import logger

if __name__ == "__main__":
    try:
        controller()
    except Exception as e:
        logger.critical(f"Unhandled exception in main: {e}")
        exit(1)
