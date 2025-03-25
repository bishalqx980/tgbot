import os
import requests

def fetch_latest_commit(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    try:
        response = requests.get(url)
        if not response.ok:
            print(response.text)
            return
        
        commits_data = response.json()
        latest_commit = commits_data[0]
        return latest_commit
    except Exception as e:
        print(e)

def send_message(bot_token, chat_id, text):
    req_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": True,
        "parse_mode": "HTML"
    }

    try:
        response = requests.get(req_url, data)
        if response.ok:
            print("Message sent successfully.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(e)

# Variables 
owner = "bishalqx980"
repo = "tgbot"
bot_token = os.getenv("BOT_TOKEN")
owner_id = int(os.getenv("OWNER_ID"))
chat_id = int(os.getenv("CHAT_ID"))

# call func's
res = fetch_latest_commit(owner, repo)
if not res:
    print("Error: error getting lastest commit.")
    exit()

committer = res['commit']['committer']
lastest_commit_url = res['html_url']
commit_message = res['commit']['message']

msg = (
    f"A new commit has been made to <a href='https://github.com/{owner}/{repo}'>{repo}</a>\n\n"
    f"<b>Latest commit:</b> <a href='{lastest_commit_url}'>{res['sha'][:7]}</a>\n"
    f"<b>Commit message:</b>\n\n"
    f"<blockquote>{commit_message}</blockquote>\n\n"
    f"<b>Committed by:</b> <i>{committer['name']}</i>"
)

sent_msg = send_message(bot_token, chat_id, f"<b>{msg}</b>")
