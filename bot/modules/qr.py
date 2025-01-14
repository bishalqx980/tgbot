import requests
from bot import logger

class QR:
    async def gen_qr(data):
        url = f"https://api.qrserver.com/v1/create-qr-code/?size=1024x1024&data={data}"
        f_name = f"downloads/qr_code.png"
        try:
            req = requests.get(url)
            open(f_name, "wb").write(req.content)
            return f_name
        except Exception as e:
            logger.error(e)
