from bot import logger

class Utils:
    @staticmethod
    def calculator(math):
        """
        solves normal maths: supported syntax: (+, -, *, /)
        """
        try:
            solved_math = eval(math)
            return True, solved_math
        except Exception as e:
            logger.error(e)
            return False, e
