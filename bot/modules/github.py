import requests
from bot import logger

class GitHub:
    async def get_latest_commit(owner, repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        try:
            res = requests.get(url)
            if not res.status_code == 200:
                return res.text
            
            commits_data = res.json()
            latest_commit = commits_data[0]
            return latest_commit
        except Exception as e:
            logger.error(e)
