import requests
from bot import logger

async def ping_url(ping_url):
  ping_time= "~ infinite"
  status_code = None

  try:
    response = requests.get(ping_url)
    status_code = response.status_code
    if status_code != 200:
      return True, ping_time, status_code
    
    ping_time = response.elapsed.total_seconds() * 1000
    ping_time = f"{int(ping_time)}ms"
    return True, ping_time, status_code
  except Exception as e:
    logger.error(e)
    return None, e