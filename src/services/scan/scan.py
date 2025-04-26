import os
from datetime import datetime

import win32com.client
from PIL import Image

from src.utils.logger import logger


def scan(save_dir="resources/output/scans"):
    try:
        wia_dialog = win32com.client.Dispatch("WIA.CommonDialog")
    except Exception as e:
        logger.error(f"[Xatolik] WIA interfeysi ishga tushmadi: {e}")
        return None

    try:
        device = wia_dialog.ShowSelectDevice()
        if not device:
            logger.error("[Ogohlantirish] Qurilma tanlanmadi.")
            return None
        logger.info(f"✔ Tanlangan qurilma: {device.Properties['Name'].Value}")
    except Exception as e:
        logger.error(f"[Xatolik] Qurilma tanlashda xatolik: {e}")
        return None

    try:
        item = device.Items[0]
        item.Properties["6146"].Value = 1
        item.Properties["6147"].Value = 300
        item.Properties["6148"].Value = 300
        item.Properties["6151"].Value = 2480
        item.Properties["6152"].Value = 3508
    except Exception as e:
        logger.error(f"[Xatolik] Parametrlarni o‘rnatishda muammo: {e}")
        return None

    try:
        logger.info("📠 Skaner ishlamoqda...")
        image = wia_dialog.ShowTransfer(item, "{B96B3CAF-0728-11D3-9D7B-0000F81EF32E}")
    except Exception as e:
        logger.error(f"[Xatolik] Skan qilishda muammo: {e}")
        return None

    try:
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        jpg_path = os.path.join(save_dir, f"scan_{timestamp}.jpg")
        pdf_path = os.path.join(save_dir, f"scan_{timestamp}.pdf")

        image.SaveFile(jpg_path)
        logger.info(f"🖼 Rasm JPG ko‘rinishida saqlandi: {jpg_path}")

        with Image.open(jpg_path) as img:
            rgb_image = img.convert("RGB")
            rgb_image.save(pdf_path, "PDF", resolution=100.0)

        logger.info(f"✅ PDF fayl yaratildi: {pdf_path}")

        os.remove(jpg_path)
        return pdf_path

    except Exception as e:
        logger.error(f"[Xatolik] Faylni PDFga o‘tkazishda xatolik: {e}")
        return None
