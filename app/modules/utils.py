import random
import string
import pyzipper
from time import time
from io import BytesIO
from aiohttp import ClientSession, ClientTimeout
from app import logger


class UTILITY:
    @staticmethod
    def createProgressBar(percentValue: int, barSize: int = 10) -> str:
        """
        :param percentValue: `int`
        :param barSize: `int` default 10
        :returns str: Progress Bar
        """
        emptySymbol = "▱"
        fullSymbol = "▰"

        barFilled = int(barSize * (int(percentValue) / 100))
        barEmpty = int(barSize - barFilled)

        return f"[ {fullSymbol * barFilled}{emptySymbol * barEmpty} ]"
    

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
            return eval(math)
        except Exception as e:
            logger.error(e)
            return str(e)
    

    @staticmethod
    async def pingServer(url: str, timeout: int = 5) -> str:
        try:
            async with ClientSession() as session:
                start_time = time()
                async with session.get(url, timeout=ClientTimeout(timeout)) as response:
                    response_time = int((time() - start_time) * 1000) # converting to ms

                    if response_time > 1000:
                        server_ping = f"{(response_time / 1000):.2f}s"
                    else:
                        server_ping = f"{response_time}ms"
                    
                    return server_ping
        except:
            return "~ infinite ~"
    

    @staticmethod
    def unzipFile(path, password = None, extraction_path: str = "downloads"):
        """
        :param path: file path or bytes\n
        :returns list: file path list
        """
        FILEPATH_LIST = []

        try:
            try:
                with pyzipper.AESZipFile(path) as archiveFile:
                    if password: archiveFile.setpassword(password.encode())
                    archiveFile.extractall(extraction_path)
            except:
                with pyzipper.ZipFile(path) as archiveFile:
                    if password: archiveFile.setpassword(password.encode())
                    archiveFile.extractall(extraction_path)
            
            name_list = archiveFile.namelist()
            for i in name_list:
                FILEPATH_LIST.append(f"{extraction_path}/{i}")
            return FILEPATH_LIST
        except Exception as e:
            logger.error(e)
            return e
    

    @staticmethod
    def makeMemoryFile(content: bytes):
        try:
            buffer = BytesIO()
            buffer.write(content)
            buffer.seek(0)
            return buffer
        except Exception as e:
            logger.error(e)


    @staticmethod
    def to_monospace(text: str) -> str:
        result = []

        for c in text:
            if "A" <= c <= "Z":
                result.append(chr(ord("𝙰") + ord(c) - ord("A")))
            elif "a" <= c <= "z":
                result.append(chr(ord("𝚊") + ord(c) - ord("a")))
            elif "0" <= c <= "9":
                result.append(chr(ord("𝟶") + ord(c) - ord("0")))
            else:
                result.append(c)

        return "".join(result)
