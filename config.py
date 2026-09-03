import os
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# HELPERS
# ============================================================

def get_env(name, default=None):
    """Get environment variable and remove extra spaces."""
    value = os.getenv(name, default)

    if value is None:
        return None

    return str(value).strip()


def get_int(name, default=0):
    """Safely convert environment variable to integer."""
    value = get_env(name)

    if value in (None, ""):
        return default

    try:
        return int(value)
    except (TypeError, ValueError):
        raise RuntimeError(
            f"{name} must be a valid integer."
        )


# ============================================================
# CONFIG
# ============================================================

class Config:

    # --------------------------------------------------------
    # TELEGRAM
    # --------------------------------------------------------

    API_ID = get_int(
        "API_ID",
        0
    )

    API_HASH = get_env(
        "API_HASH",
        ""
    )

    BOT_TOKEN = get_env(
        "BOT_TOKEN",
        ""
    )

    OWNER_ID = get_int(
        "OWNER_ID",
        0
    )


    # --------------------------------------------------------
    # MONGODB
    # --------------------------------------------------------

    MONGO_URL = get_env(
        "MONGO_URL",
        ""
    )

    DB_NAME = get_env(
        "DB_NAME",
        "kirti_api"
    )


    # --------------------------------------------------------
    # START IMAGE
    # --------------------------------------------------------

    START_IMAGE = get_env(
        "START_IMAGE",
        "https://n.uguu.se/RtoiNEur.jpg"
    )


    # --------------------------------------------------------
    # BUTTON LINKS
    # --------------------------------------------------------

    UPDATES_URL = get_env(
        "UPDATES_URL",
        "https://t.me/annu_updates"
    )

    SUPPORT_URL = get_env(
        "SUPPORT_URL",
        "https://t.me/annu_support"
    )


    # --------------------------------------------------------
    # API SETTINGS
    # --------------------------------------------------------

    API_NAME = get_env(
        "API_NAME",
        "KIRTI API"
    )

    API_DOMAIN = get_env(
        "API_DOMAIN",
        "http://yt-music-api-seven.vercel.app"
    ).rstrip("/")


    # --------------------------------------------------------
    # LIMIT / TIER
    # --------------------------------------------------------

    DAILY_LIMIT = get_int(
        "DAILY_LIMIT",
        6000
    )

    TIER = get_env(
        "TIER",
        "FREE"
    )


    # ========================================================
    # VALIDATION
    # ========================================================

    @classmethod
    def validate(cls):

        missing = []

        if cls.API_ID <= 0:
            missing.append("API_ID")

        if not cls.API_HASH:
            missing.append("API_HASH")

        if not cls.BOT_TOKEN:
            missing.append("BOT_TOKEN")

        if not cls.MONGO_URL:
            missing.append("MONGO_URL")

        if not cls.DB_NAME:
            missing.append("DB_NAME")

        if not cls.START_IMAGE:
            missing.append("START_IMAGE")

        if not cls.API_DOMAIN:
            missing.append("API_DOMAIN")

        if not cls.UPDATES_URL:
            missing.append("UPDATES_URL")

        if not cls.SUPPORT_URL:
            missing.append("SUPPORT_URL")

        if cls.DAILY_LIMIT <= 0:
            raise RuntimeError(
                "DAILY_LIMIT must be greater than 0."
            )

        if missing:
            raise RuntimeError(
                "Missing required environment variables: "
                + ", ".join(missing)
            )

        return True


# ============================================================
# VALIDATE CONFIG
# ============================================================

Config.validate()


# ============================================================
# STARTUP INFO
# ============================================================

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🚀 KIRTI API BOT CONFIG LOADED")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"🗄️ Database : {Config.DB_NAME}")
print(f"🌐 API      : {Config.API_DOMAIN}")
print(f"💎 Tier     : {Config.TIER}")
print(f"📊 Limit    : {Config.DAILY_LIMIT}/day")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
