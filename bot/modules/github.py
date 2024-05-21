import requests

class GitHub:
    async def get_latest_commit(owner, repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        res = requests.get(url)

        if res.status_code == 200:
            commits_data = res.json()
            latest_commit = commits_data[0]
            return latest_commit
        else:
            print(f"Error: {res.status_code}")
            return
        