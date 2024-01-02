from bot import safone_api

class Safone:
    async def safone_ai(msg):
        chatgpt_res = None
        bard_res = None
        chatbot_res = None
        try:
            chatgpt_res = await safone_api.chatgpt(msg)
        except Exception as e:
            print(f"Error ChatGPT: {e}")
            try:
                bard_res = await safone_api.bard(msg)
            except Exception as e:
                print(f"Error Bard: {e}")
                try:
                    chatbot_res = await safone_api.chatbot(msg)
                except Exception as e:
                    print(f"Error Chatbot: {e}")
        return chatgpt_res, bard_res, chatbot_res


    async def webshot(url):
        try:
            res = await safone_api.webshot(url)
        except Exception as e:
            print(f"Error Webshot: {e}")
        return res


    async def imagine(promt):
        try:
            res = await safone_api.imagine(promt)
            res = res[0]
        except Exception as e:
            print(f"Error youtube: {e}")
        return res
            