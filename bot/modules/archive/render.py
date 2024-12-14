import requests
from bot import logger, render_api

class Render:
    async def list_services():
        if not render_api:
            logger.error("render_api not found!")
            return
        
        url = "https://api.render.com/v1/services?limit=5"

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {render_api}"
        }

        response = requests.get(url, headers=headers)

        return response
    

    async def restart(serviceId):
        if not render_api:
            logger.error("render_api not found!")
            return
        
        url = f"https://api.render.com/v1/services/{serviceId}/restart"

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {render_api}"
        }

        response = requests.post(url, headers=headers)

        return response
    

    async def redeploy(serviceId, clear_cache=True):
        if not render_api:
            logger.error("render_api not found!")
            return
        
        url = f"https://api.render.com/v1/services/{serviceId}/deploys"

        clear_cache = "clear" if clear_cache else "do_not_clear"

        payload = { "clearCache": clear_cache }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {render_api}"
        }

        response = requests.post(url, json=payload, headers=headers)

        return response
