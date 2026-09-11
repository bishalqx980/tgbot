from typing import Optional

class CONFIG:
    def __init__(self):
        self.api_id: Optional[int] = None         # INT Get from > https://my.telegram.org/
        self.api_hash: Optional[str] = None       # STR Get from > https://my.telegram.org/
        self.bot_token: Optional[str] = None      # STR Get from > https://t.me/BotFather
        self.owner_id: Optional[int] = None       # INT After bot starts use /id

        self.mongodb_uri: Optional[str] = None    # STR Get from > https://www.mongodb.com/
        self.db_name: Optional[str] = None        # STR Anything you like (unchangeable)

        self.shrinkme_api: Optional[str] = None   # STR Get from > https://shrinkme.io/
        self.omdb_api: Optional[str] = None       # STR Get from > https://www.omdbapi.com/
        self.forecast_api: Optional[str] = None    # STR Get from > https://www.weatherapi.com/
    
    
    def validate(self) -> bool:
        """Check if required configurations are present"""
        return all([
            self.bot_token,
            self.mongodb_uri,
            self.db_name
        ])
