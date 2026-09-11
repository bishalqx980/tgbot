import qrcode
from uuid import uuid4
from io import BytesIO
from pyzbar.pyzbar import decode
from PIL import Image
from app import logger


class QR:
    @staticmethod
    def GenerateQR(data: str, size: int = 50):
        """
        ***Generate's a QR code and returns BytesIO (PNG format).***\n

        :param data: Text, URL, etc.
        :param size: Box size (multiplies to determine final image size).
        :returns: Bytes of the QR code image (PNG format).
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

            buffer = BytesIO()
            buffer.name = f"qr_{uuid4().hex}.png"
            img.save(buffer, "PNG")

            buffer.seek(0)

            return buffer
        except Exception as e:
            logger.error(e)
    

    @staticmethod
    def DecodeQR(image):
        """
        :param image: bytes or image path
        :returns ?:
        """
        try:
            return decode(Image.open(image))[0]
        except Exception as e:
            logger.error(e)
