from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from bot import logger

class KeyboardBuilder:
    def __init__(self):
        self.keyboard = []
    

    def ubutton(self, data):
        """
        **url button maker**\n
        :param data: `list` of `dict`\n
        *Note: same data in one `dict` will be in same row*
        """
        try:
            self.keyboard.clear()
            for keyboard_data in data:
                button = [InlineKeyboardButton(btn_name, btn_url) for btn_name, btn_url in keyboard_data.items()]
                self.keyboard.append(button)

            return InlineKeyboardMarkup(self.keyboard)
        except Exception as e:
            logger.error(e)


    def cbutton(self, data):
        """
        **callback button maker (also works for url btn) also including `inlineQuery`**\n
        > **This function work for both url and callback button maker if `data` starts with `http` otherwise you can use `ubutton` function to make url btn**\n
        :param data: `list` of `dict`\n
        *Note: same data in one `dict` will be in same row*\n
        *Demo for inlineQuery button: {"Try inline": "switch_to_inline"}*
        """
        try:
            self.keyboard.clear()
            for keyboard_data in data:
                row = []
                for btn_name, btn_data in keyboard_data.items():
                    if btn_data == "switch_to_inline":
                        switch_to_inline = ""
                        btn_url = None
                        callback_data = None
                    else:
                        switch_to_inline = None
                        btn_url = btn_data if btn_data.startswith("http") else None
                        callback_data = btn_data if not btn_url else None
                    
                    row.append(InlineKeyboardButton(btn_name, btn_url, callback_data, switch_inline_query_current_chat=switch_to_inline))
                
                self.keyboard.append(row)

            return InlineKeyboardMarkup(self.keyboard)
        except Exception as e:
            logger.error(e)
