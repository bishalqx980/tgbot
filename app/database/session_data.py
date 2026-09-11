from typing import Union

from app import logger


class SessionStorage:
    def __init__(self):
        self.data_center = {}
    

    def insert(self, identifier: Union[str, int] = None, data: dict = None):
        """
        :param identifier (optional): key to find/store the data | example: chat.id `optional` "if not given, data will be inserted directly"
        """
        if not data:
            logger.error("Error: SessionData 'data' parameter wasn't given.")
            return
        
        if identifier:
            load_data = self.data_center.get(identifier, {})
            if load_data:
                load_data.update(data)
            else:
                self.data_center[identifier] = data
        else:
            self.data_center.update(data) # direct data insert
    

    def get(self, key, default = None):
        """
        :param key: data you are looking for (inserted as identifier) / the direct data name
        """
        return self.data_center.get(key, default)


    def clear_all(self):
        self.data_center.clear()
