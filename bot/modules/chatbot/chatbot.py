import json
import random

CHATBOT_DB_PATH = "bot/modules/chatbot/chatbot_db.json"

with open(CHATBOT_DB_PATH) as f:
    chatbot_db = json.load(f)

async def chatbot(prompt):
    response = None
    for key, value in chatbot_db.items():
        for word in value["words"]:
            if word in prompt.lower():
                response = random.choice(value["responses"])
                return response
