import aiohttp
from bot import logger

class QR:
    async def gen_qr(data, file_name="image"):
        url = f"https://api.qrserver.com/v1/create-qr-code/?size=1024x1024&data={data}"
        f_name = f"downloads/{file_name}.png"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return
                    
                    content = await response.read()
                    open(f_name, "wb").write(content)
                    return f_name
        except Exception as e:
            logger.error(e)
