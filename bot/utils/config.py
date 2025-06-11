import os
from dotenv import load_dotenv
from typing import Optional

class CONFIG:
    def __init__(self):
        """Initialize with None values"""
        self.bot_token: Optional[str] = None
        self.owner_id: Optional[int] = None
        self.show_bot_pic: bool = False # Default Value
        self.server_url: Optional[str] = None

        self.mongodb_uri: Optional[str] = None
        self.db_name: Optional[str] = None

        self.shrinkme_api: Optional[str] = None
        self.omdb_api: Optional[str] = None
        self.weather_api: Optional[str] = None


    def load_config(self, config_file) -> None:
        """
        Load configuration from .env file\n
        :param config_file: .env file path
        """
        load_dotenv(config_file)

        # ----- BOT CONFIGURATION -----
        self.bot_token = os.getenv("BOT_TOKEN")
        self.owner_id = int(os.getenv("OWNER_ID") or 0)
        
        # ----- DATABASE -----
        self.mongodb_uri = os.getenv("MONGODB_URI")
        self.db_name = os.getenv("DB_NAME")

        # ----- API KEYS -----
        self.shrinkme_api = os.getenv("SHRINKME_API")
        self.omdb_api = os.getenv("OMDB_API")
        self.weather_api = os.getenv("WEATHER_API")
    

    def validate(self) -> bool:
        """Check if required configurations are present"""
        required = [
            self.bot_token,
            self.mongodb_uri,
            self.db_name
        ]

        return all(required)
