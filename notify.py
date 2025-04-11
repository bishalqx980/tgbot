import os
import requests

GITHUB_OWNER_USERNAME = "bishalqx980"
REPO_NAME = "tgbot"
# telegram variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID")) # chat_id to send update message; could be owner_id

def main():
    # get commit
    try:
        response = requests.get(f"https://api.github.com/repos/{GITHUB_OWNER_USERNAME}/{REPO_NAME}/commits")
        if not response.ok:
            print(response.text)
            return
        
        commits_data = response.json()
        latest_commit = commits_data[0]

        committer = latest_commit['commit']['committer']
        latest_commit_url = latest_commit['html_url']
        commit_message = latest_commit['commit']['message']

        message = (
            f"A new <b><a href='{latest_commit_url}'>commit {latest_commit['sha'][:7]}</a></b> has been made to <a href='https://github.com/{GITHUB_OWNER_USERNAME}/{REPO_NAME}'>{REPO_NAME}</a>\n\n"

            f"<blockquote>{commit_message}</blockquote>\n\n"

            f"<b>Signed by:</b> <i>{committer['name']}</i>"
        )

        data = {
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": True,
            "parse_mode": "HTML"
        }

        response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data)
        if response.ok:
            print("Message sent successfully.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(e)

# calling the function
main()
