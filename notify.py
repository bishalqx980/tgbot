import os
import json
import requests

# Constants
GITHUB_OWNER_USERNAME = "bishalqx980"
REPO_NAME = "tgbot"
# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID") # chat_id to send update message; could be owner_id


def getGitcommits():
    """:returns dict: json dict"""
    response = requests.get(f"https://api.github.com/repos/{GITHUB_OWNER_USERNAME}/{REPO_NAME}/commits")
    if not response.ok:
        print(response.text)
        return
    
    return response.json()


def apiReq(method, data):
    """
    :param method: `str` name of method example: setMessageReaction
    :param data: `dict`
    """
    response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/{method}", data)
    if response.ok:
        print("Request Successful...!")
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")


def main():
    # get commit
    commits_data = getGitcommits()
    if not commits_data:
        return
    
    latest_commit = commits_data[0]

    committer = latest_commit['commit']['committer']
    latest_commit_url = latest_commit['html_url']
    commit_message = latest_commit['commit']['message']

    message = (
        f"A new <b><a href='{latest_commit_url}'>commit {latest_commit['sha'][:7]}</a></b> has been made to <a href='https://github.com/{GITHUB_OWNER_USERNAME}/{REPO_NAME}'>{REPO_NAME}</a>\n\n"

        f"<blockquote>{commit_message}</blockquote>\n\n"

        f"<b>Signed by:</b> <i>{committer['name']}</i>"
    )

    sendMessageData = {
        "chat_id": int(CHAT_ID),
        "text": message,
        "disable_web_page_preview": True,
        "parse_mode": "HTML"
    }

    res = apiReq("sendMessage", sendMessageData)
    if not res:
        return
    
    setMessageReactionData = {
        "chat_id": int(CHAT_ID),
        "message_id": res["result"]["message_id"],
        "reaction": json.dumps([{"type": "emoji", "emoji": "🔥"}]),
        "is_big": True
    }

    apiReq("setMessageReaction", setMessageReactionData)

# calling the function
if all([BOT_TOKEN, CHAT_ID, GITHUB_OWNER_USERNAME, REPO_NAME]):
    main()
