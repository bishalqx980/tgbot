import qrcode
from bot import logger

class QR:
    def generate_qr(data, file_name="qrcode", size=50):
        """
        :param data: text, url etc.\n
        ***Note: `size` multiply with (29 * size = image_pixels)***
        """
        try:
            qr = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=size,
                border=4,
            )

            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            file_path = f"temp/{file_name}.png"
            img.save(file_path)
            return file_path
        except Exception as e:
            logger.error(e)
