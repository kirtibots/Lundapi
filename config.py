import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_ID = int(os.getenv("API_ID", "21692000"))
    API_HASH = os.getenv(
        "API_HASH",
        "1e37856155373adf855c061c49847ced"
    )
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")

    MONGO_URL = os.getenv(
        "MONGO_URL",
        "mongodb://localhost:27017"
    )

    DB_NAME = os.getenv(
        "DB_NAME",
        "kirti_api"
    )

    OWNER_ID = int(
        os.getenv("OWNER_ID", "0")
    )


    # ========================================================
    # START IMAGE
    # ========================================================

    START_IMAGE = os.getenv(
        "START_IMAGE",
        "https://n.uguu.se/RtoiNEur.jpg"
    )


    # ========================================================
    # BUTTONS / LINKS
    # ========================================================

    UPDATES_URL = os.getenv(
        "UPDATES_URL",
        "https://t.me/annu_updates"
    )

    SUPPORT_URL = os.getenv(
        "SUPPORT_URL",
        "https://t.me/annu_support"
    )


    # ========================================================
    # API DISPLAY SETTINGS
    # ========================================================

    API_NAME = os.getenv(
        "API_NAME",
        "KIRTI API"
    )

    API_DOMAIN = os.getenv(
        "API_DOMAIN",
        "http://yt-music-api-seven.vercel.app"
    )

    DAILY_LIMIT = int(
        os.getenv("DAILY_LIMIT", "6000")
    )

    TIER = os.getenv(
        "TIER",
        "FREE"
    )


    # ========================================================
    # VALIDATE
    # ========================================================

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
            raise RuntimeError(
                "Missing environment variables: "
                + ", ".join(missing)
            )


Config.validate()
