import requests
from bot import logger

async def upload_image(image_path):
    """
    returns `json` response
    """
    api_key = "6d207e02198a847aa98d0a2a901485a5" # public access api key
    url = "https://freeimage.host/api/1/upload"

    # files = {
    #     "source": open(image_path, "rb")
    # }

    params = {
        "key": api_key, # API Key
        "action": "upload", # What you want to do [values: upload].
        "source": image_path, # img url or base64 string
        "format": "json" # Sets the return format [values: json (default), redirect, txt].
    }

    try:
        req = requests.post(url, params, timeout=3) # files=files
        return True, req.json()
    except requests.Timeout as e:
        logger.error(e)
        return False, e
    except Exception as e:
        logger.error(e)
