import qrcode
from io import BytesIO
from pyzbar.pyzbar import decode
from PIL import Image
from bot import logger

class QR:
    @staticmethod
    def generate_qr(data, size=50):
        """
        Generate a QR code and return it as bytes (PNG format).\n
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

            img_buffer = BytesIO()
            img.save(img_buffer, "PNG")
            img_buffer.seek(0)

            return img_buffer.read()
        except Exception as e:
            logger.error(e)
    

    @staticmethod
    def decode_qr(image_data):
        """
        :param image_data: byte or image path
        :returns ?:
        """
        try:
            decoded_objects = decode(Image.open(image_data))
            return decoded_objects[0]
        except Exception as e:
            logger.error(e)
