import aiohttp
from typing import Union
from base64 import b64encode
from app import logger


async def UploadImage(image: Union[str, bytes]):
    """
    :param image: localpath / bytes
    :return dict:
    """
    api_key = "6d207e02198a847aa98d0a2a901485a5" # public access api key
    url = "https://freeimage.host/api/1/upload"

    data = {
        "key": api_key, # API Key
        "action": "upload", # What you want to do [values: upload].
        # "source": image, # img URL or base64 string or local path
        "format": "json" # Sets the return format [values: json (default), redirect, txt].
    }

    # I will handle localpath and bytes only (not URL's)
    if isinstance(image, bytes):
        data["source"] = b64encode(image).decode("UTF-8")
    elif isinstance(image, str):
        with open(image, "rb") as f:
            # even its a localfile but im treating as base64
            data["source"] = b64encode(f.read()).decode("UTF-8")

            # data = aiohttp.FormData()
            # data.add_field(
            #     "source",
            #     f,
            #     filename="image.png",
            #     content_type="application/octet-stream"
            # )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                return await response.json()
    except Exception as e:
        logger.error(e)
        return str(e)
