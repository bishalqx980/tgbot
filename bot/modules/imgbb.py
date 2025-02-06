import requests
from bot import logger
# from base64 import b64encode
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE

async def imgbb_upload(image_url, file_name):
    imgbb_api = await LOCAL_DATABASE.get_data("bot_docs", "imgbb_api")
    if not imgbb_api:
        imgbb_api = await MongoDB.get_data("bot_docs", "imgbb_api")
        if not imgbb_api:
            logger.error("imgbb_api not found!")
            return False

    try:
        post_url = "https://api.imgbb.com/1/upload"

        # img_data = open(image_path, "rb").read()
        # img_b64 = b64encode(img_data)

        payload = {
            "key": imgbb_api,
            "image": image_url,
            "name": file_name
        }

        req = requests.post(post_url, payload, timeout=3)
        if req.status_code == 200:
            return_data = req.json()
        else:
            return_data = None
        
        return return_data
    except Exception as e:
        logger.error(e)
