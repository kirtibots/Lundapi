import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "meow_api")
    OWNER_ID = int(os.getenv("OWNER_ID", "0"))

    # Buttons / links
    UPDATES_URL = os.getenv("UPDATES_URL", "https://t.me/your_updates")
    SUPPORT_URL = os.getenv("SUPPORT_URL", "https://t.me/your_support")

    # API display settings
    API_NAME = os.getenv("API_NAME", "KIRTI API")
    API_DOMAIN = os.getenv("API_DOMAIN", "https://music.example.com")
    DAILY_LIMIT = int(os.getenv("DAILY_LIMIT", "6000"))
    TIER = os.getenv("TIER", "FREE")

    @classmethod
    def validate(cls):
        missing = []
        if not cls.API_ID:
            missing.append("API_ID")
        if not cls.API_HASH:
            missing.append("API_HASH")
        if not cls.BOT_TOKEN:
            missing.append("BOT_TOKEN")
        if missing:
            raise RuntimeError("Missing environment variables: " + ", ".join(missing))

Config.validate()
