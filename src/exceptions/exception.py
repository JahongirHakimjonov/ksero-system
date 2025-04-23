from src.utils.logger import logger


class UnsupportedFileTypeError(Exception):
    """Custom exception for unsupported file types."""

    def __init__(self, message):
        super().__init__(message)
        logger.error(message)
        self.message = message
