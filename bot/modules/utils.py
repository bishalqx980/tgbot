import random
import string
from bot import logger

class Utils:
    @staticmethod
    def createProgressBar(percentValue, barSize=10) -> str:
        """
        :param percentValue: `int`
        :param barSize: `int` default 10
        :returns str: Progress Bar
        """
        emptySymbol = "▱"
        fullSymbol = "▰"

        barFilled = int(barSize * (int(percentValue) / 100))
        barEmpty = int(barSize - barFilled)

        barStr = f"[ {fullSymbol * barFilled}{emptySymbol * barEmpty} ]"
        return barStr
    

    @staticmethod
    def randomString(length: int = 16) -> str:
        """
        Generates a random string with a mix of:
        - hexdigits
        - octdigits
        """
        return "".join(random.choice(string.hexdigits + string.octdigits) for _ in range(length))


    @staticmethod
    def calculator(math) -> tuple[bool, float | int | str]:
        """
        solves normal maths: supported syntax: (+, -, *, /)
        """
        try:
            solved_math = eval(math)
            return True, solved_math
        except Exception as e:
            logger.error(e)
            return False, e
