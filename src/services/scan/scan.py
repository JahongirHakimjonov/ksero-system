import os
from datetime import datetime
from io import BytesIO

import PIL.Image
import twain

from src.utils.logger import logger

scanned_image = None


def scan() -> tuple[str, str] | None:
    """
    Scans a document using a TWAIN-compatible scanner, saves as PNG and PDF,
    and returns the paths of the saved files.
    """
    global scanned_image
    output_dir = os.path.join("resources", "output")
    os.makedirs(output_dir, exist_ok=True)

    try:
        with twain.SourceManager(0) as sm:
            src = sm.open_source()
            if not src:
                logger.warning("No scanner source selected (user may have cancelled).")
                return None

            logger.info("Acquiring image from scanner...")
            src.request_acquire(show_ui=False, modal_ui=False)
            handle, _ = src.xfer_image_natively()
            bmp_bytes = twain.dib_to_bm_file(handle)

            img = PIL.Image.open(BytesIO(bmp_bytes), formats=["bmp"])
            width, height = img.size
            factor = 600.0 / width
            resized_img = img.resize((int(width * factor), int(height * factor)))
            scanned_image = resized_img

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            png_path = os.path.join(output_dir, f"scanned_{timestamp}.png")
            pdf_path = os.path.join(output_dir, f"scanned_{timestamp}.pdf")

            resized_img.save(png_path, "PNG")
            resized_img.save(pdf_path, "PDF")

            logger.info(f"Scanned image saved as: {png_path} and {pdf_path}")
            return png_path, pdf_path

    except Exception as e:
        logger.exception(f"Scanning failed: {e}")
        return None
