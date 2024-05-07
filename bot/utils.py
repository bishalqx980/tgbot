from bot import logger

def calc(math):
    try:
        return eval(math)
    except Exception as e:
        error_msg = f"Error Math: {e}"
        logger.error(error_msg)
        return error_msg