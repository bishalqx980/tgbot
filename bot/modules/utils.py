from bot import logger

class Utils:
    @staticmethod
    def createProgressBar(percentValue, barSize=10):
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
