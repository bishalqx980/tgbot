from bot import logger
from SafoneAPI import SafoneAPI

safone_api = SafoneAPI()

class Safone:
    async def safone_ai(msg):
        chatgpt_res, bard_res, chatbot_res = None, None, None
        try:
            chatgpt_res = await safone_api.chatgpt(msg)
        except Exception as e:
            logger.error(e)
            try:
                bard_res = await safone_api.bard(msg)
            except Exception as e:
                logger.error(e)
                try:
                    chatbot_res = await safone_api.chatbot(msg)
                except Exception as e:
                    logger.error(e)
        return chatgpt_res, bard_res, chatbot_res


    async def webshot(url):
        try:
            res = await safone_api.webshot(url)
            return res
        except Exception as e:
            logger.error(e)


    async def imagine(prompt):
        try:
            res = await safone_api.imagine(prompt)
            res = res[0]
            return res
        except Exception as e:
            logger.error(e)
