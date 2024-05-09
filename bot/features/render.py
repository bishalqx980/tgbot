import requests
from bot import render_api

class Render:
    async def list_services():
        url = "https://api.render.com/v1/services?limit=20"

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {render_api}"
        }

        response = requests.get(url, headers=headers)

        return response
    

    async def restart(serviceId):
        url = f"https://api.render.com/v1/services/{serviceId}/restart"

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {render_api}"
        }

        response = requests.post(url, headers=headers)

        return response
    

    async def redeploy(serviceId, clear_cache=True):
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
