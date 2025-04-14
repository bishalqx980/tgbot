from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from .. import logger

class ButtonMaker:
    def ubutton(data):
        """
        **url button maker**\n
        :param data: `list` of `dict`\n
        *Note: same data in one `dict` will be in same row*
        """
        try:
            keyboard = []
            for keyboard_data in data:
                button = [InlineKeyboardButton(btn_name, btn_url) for btn_name, btn_url in keyboard_data.items()]
                keyboard.append(button)

            return InlineKeyboardMarkup(keyboard)
        except Exception as e:
            logger.error(e)


    def cbutton(data):
        """
        **callback button maker (also works for url btn)**\n
        > **This function work for both url and callback button maker if `data` starts with `http` otherwise you can use `ubutton` function to make url btn**\n
        :param data: `list` of `dict`\n
        *Note: same data in one `dict` will be in same row*
        """
        try:
            keyboard = []
            for keyboard_data in data:
                row = []
                for btn_name, btn_data in keyboard_data.items():
                    btn_url = btn_data if btn_data.startswith("http") else None
                    callback_data = btn_data if not btn_url else None
                    
                    row.append(InlineKeyboardButton(btn_name, btn_url, callback_data))
                
                keyboard.append(row)

            return InlineKeyboardMarkup(keyboard)
        except Exception as e:
            logger.error(e)
