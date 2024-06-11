from bot import logger

async def calculator(math):
    try:
        solved_math = eval(math)
        return True, solved_math
    except Exception as e:
        logger.error(e)
        return False, e
