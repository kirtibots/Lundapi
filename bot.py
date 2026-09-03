import asyncio
import secrets
import string
from datetime import datetime, timezone

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from motor.motor_asyncio import AsyncIOMotorClient

from config import Config





# ============================================================
# PREMIUM UI STYLE
# ============================================================

_FONT_NORMAL = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
_FONT_BOLD = (
    "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"
    "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
)
_FONT_MAP = str.maketrans(_FONT_NORMAL, _FONT_BOLD)

def sf(text: str) -> str:
    """Premium bold Unicode style for normal UI text."""
    return text.translate(_FONT_MAP)


# ============================================================
# DATABASE
# ============================================================

mongo = AsyncIOMotorClient(Config.MONGO_URL)
db = mongo[Config.DB_NAME]
users = db.users


# ============================================================
# BOT
# ============================================================

app = Client(
    "meow_api_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
)


# ============================================================
# HELPERS
# ============================================================

def now():
    return datetime.now(timezone.utc)


def make_api_key(length=32):
    alphabet = string.ascii_letters + string.digits
    return "kirti_" + "".join(secrets.choice(alphabet) for _ in range(length))


async def get_user(user_id: int):
    return await users.find_one({"user_id": user_id})


async def create_user(user_id: int, first_name: str = "User"):
    key = make_api_key()
    doc = {
        "user_id": user_id,
        "first_name": first_name,
        "api_key": key,
        "tier": Config.TIER,
        "status": "ACTIVE",
        "requests_today": 0,
        "total_requests": 0,
        "data_streamed": 0,
        "created_at": now(),
        "last_refresh": now(),
    }
    await users.update_one(
        {"user_id": user_id},
        {"$setOnInsert": doc},
        upsert=True,
    )
    return await get_user(user_id)


async def regenerate_key(user_id: int):
    key = make_api_key()
    await users.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "api_key": key,
                "status": "ACTIVE",
                "last_refresh": now(),
            }
        },
    )
    return await get_user(user_id)


def api_key_short(key: str):
    # Keep the key readable but avoid displaying too much in notifications/logs.
    if len(key) <= 16:
        return key
    return key[:10] + "..." + key[-6:]


def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔑 𝗚𝗘𝗧 𝗔𝗣𝗜 𝗞𝗘𝗬", callback_data="get_key"),
            InlineKeyboardButton("🔄 𝗥𝗘𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗘", callback_data="regenerate"),
        ],
        [
            InlineKeyboardButton("📖 𝗔𝗣𝗜 𝗗𝗢𝗖𝗦", callback_data="docs"),
            InlineKeyboardButton("⚡ 𝗦𝗧𝗔𝗧𝗨𝗦", callback_data="status"),
        ],
        [
            InlineKeyboardButton("📢 𝗨𝗣𝗗𝗔𝗧𝗘𝗦", url=Config.UPDATES_URL),
            InlineKeyboardButton("💬 𝗦𝗨𝗣𝗣𝗢𝗥𝗧", url=Config.SUPPORT_URL),
        ],
    ])


def key_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 𝗥𝗘𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗘", callback_data="regenerate"),
            InlineKeyboardButton("⬅️ 𝗕𝗔𝗖𝗞", callback_data="home"),
        ],
    ])


def status_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 𝗥𝗘𝗙𝗥𝗘𝗦𝗛", callback_data="status"),
            InlineKeyboardButton("⬅️ 𝗕𝗔𝗖𝗞", callback_data="home"),
        ],
    ])


def docs_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🐍 𝗣𝗬𝗧𝗛𝗢𝗡", callback_data="python_example"),
            InlineKeyboardButton("🚀 𝗖𝗨𝗥𝗟", callback_data="curl_example"),
        ],
        [
            InlineKeyboardButton("⬅️ 𝗕𝗔𝗖𝗞", callback_data="home"),
        ],
    ])


def format_home(user):
    name = user.get("first_name") or "User"
    return f"""<blockquote><b>✦ 𝗞𝗜𝗥𝗧𝗜 𝗔𝗣𝗜 ✦ 🇨🇦</b>
<code>/start</code></blockquote>

<b>╭━━━ 𝗪𝗘𝗟𝗖𝗢𝗠𝗘, {sf(name.upper())} ━━━╮</b>

<blockquote><b>🎵 𝗞𝗜𝗥𝗧𝗜 𝗠𝗨𝗦𝗜𝗖 𝗘𝗡𝗚𝗜𝗡𝗘</b>
<i>Ultra High-Speed • Lossless Audio
Streaming API • Global CDN</i></blockquote>

<blockquote><b>⚡ 𝗤𝗨𝗜𝗖𝗞 𝗦𝗧𝗔𝗥𝗧</b>
<i>Tap 「🔑 𝗚𝗘𝗧 𝗔𝗣𝗜 𝗞𝗘𝗬」 below to create
or view your personal streaming key.</i></blockquote>

<b>╰━━━ 𝗦𝗘𝗟𝗘𝗖𝗧 𝗔𝗡 𝗢𝗣𝗧𝗜𝗢𝗡 𝗕𝗘𝗟𝗢𝗪 👇 ━━━╯</b>"""

def format_key(user):
    key = user["api_key"]
    endpoint = f"{Config.API_DOMAIN}/stream/{{VIDEO_ID}}?key={key}&type=audio"
    return f"""<blockquote><b>🔐 𝗬𝗢𝗨𝗥 𝗔𝗣𝗜 𝗞𝗘𝗬</b></blockquote>

<blockquote><b>🔑 𝗔𝗖𝗧𝗜𝗩𝗘 𝗔𝗣𝗜 𝗞𝗘𝗬</b>
<code>{key}</code>
<i>Keep this key private. Do not share it publicly.</i>

• <b>𝗧𝗜𝗘𝗥:</b> {user.get("tier", Config.TIER)}
• <b>𝗦𝗧𝗔𝗧𝗨𝗦:</b> 🟢 {user.get("status", "ACTIVE")}</blockquote>

<blockquote><b>📊 𝗤𝗨𝗢𝗧𝗔 & 𝗨𝗦𝗔𝗚𝗘</b>
• <b>𝗥𝗘𝗤𝗨𝗘𝗦𝗧𝗦 𝗧𝗢𝗗𝗔𝗬:</b> {user.get("requests_today", 0)}
• <b>𝗧𝗢𝗧𝗔𝗟 𝗥𝗘𝗤𝗨𝗘𝗦𝗧𝗦:</b> {user.get("total_requests", 0)}
• <b>𝗗𝗔𝗧𝗔 𝗦𝗧𝗥𝗘𝗔𝗠𝗘𝗗:</b> {user.get("data_streamed", 0)} B
• <b>𝗗𝗔𝗜𝗟𝗬 𝗟𝗜𝗠𝗜𝗧:</b> {Config.DAILY_LIMIT} Requests / Day
• <b>𝗘𝗫𝗣𝗜𝗥𝗔𝗧𝗜𝗢𝗡:</b> Never (Lifetime)</blockquote>

<blockquote><b>🔗 𝗦𝗧𝗥𝗘𝗔𝗠 𝗘𝗡𝗗𝗣𝗢𝗜𝗡𝗧</b>
<code>{endpoint}</code></blockquote>"""

def format_status():
    return f"""<blockquote><b>📡 𝗬𝗨𝗞𝗜 𝗠𝗨𝗦𝗜𝗖 𝗦𝗧𝗔𝗧𝗨𝗦</b></blockquote>

<blockquote><b>🟢 𝗦𝗬𝗦𝗧𝗘𝗠 𝗛𝗘𝗔𝗟𝗧𝗛</b>
• <b>𝗖𝗗𝗡 𝗦𝗧𝗔𝗧𝗨𝗦:</b> 🟢 100% Operational
• <b>𝗦𝗧𝗥𝗘𝗔𝗠 𝗤𝗨𝗔𝗟𝗜𝗧𝗬:</b> 320Kbps Lossless Audio
• <b>𝗔𝗣𝗜 𝗟𝗔𝗧𝗘𝗡𝗖𝗬:</b> ~180ms Ultra-Fast
• <b>𝗣𝗥𝗢𝗧𝗢𝗖𝗢𝗟:</b> HTTP/2 + TLS 1.3 High-Speed</blockquote>

<blockquote><b>✨ 𝗚𝗟𝗢𝗕𝗔𝗟 𝗖𝗗𝗡</b>
<i>All configured edge nodes are online.</i></blockquote>"""

def format_docs():
    return f"""<blockquote><b>📚 𝗬𝗨𝗞𝗜 𝗠𝗨𝗦𝗜𝗖 𝗔𝗣𝗜 𝗗𝗢𝗖𝗨𝗠𝗘𝗡𝗧𝗔𝗧𝗜𝗢𝗡</b></blockquote>

<blockquote><b>🎧 𝗔𝗨𝗗𝗜𝗢 𝗦𝗧𝗥𝗘𝗔𝗠</b>
<code>{Config.API_DOMAIN}/stream/{{VIDEO_ID}}?key={{YOUR_KEY}}&amp;type=audio</code>

<b>ℹ️ 𝗧𝗥𝗔𝗖𝗞 𝗠𝗘𝗧𝗔𝗗𝗔𝗧𝗔</b>
<code>{Config.API_DOMAIN}/info/{{VIDEO_ID}}?key={{YOUR_KEY}}</code></blockquote>

<blockquote><b>⚙️ 𝗤𝗨𝗘𝗥𝗬 𝗣𝗔𝗥𝗔𝗠𝗘𝗧𝗘𝗥𝗦</b>
• <b>key</b> — required
• <b>type</b> — audio / video
• <b>itag</b> — optional stream format</blockquote>

<blockquote><b>💎 𝗞𝗘𝗬 𝗛𝗜𝗚𝗛𝗟𝗜𝗚𝗛𝗧𝗦</b>
• Single-call playback
• Ultra-low latency
• High-bandwidth streaming</blockquote>"""

def format_python():
    return f"""<blockquote><b>🐍 𝗣𝗬𝗧𝗛𝗢𝗡 𝗘𝗫𝗔𝗠𝗣𝗟𝗘</b></blockquote>

<pre><code>import aiohttp

API_KEY = "YOUR_API_KEY"
VIDEO_ID = "VIDEO_ID"

url = "{Config.API_DOMAIN}/stream/" + VIDEO_ID
params = {{
    "key": API_KEY,
    "type": "audio"
}}

async with aiohttp.ClientSession() as session:
    async with session.get(url, params=params) as r:
        data = await r.read()

with open("song.mp3", "wb") as f:
    f.write(data)</code></pre>"""

def format_curl():
    return f"""<blockquote><b>🚀 𝗖𝗨𝗥𝗟 / 𝗕𝗔𝗦𝗛 𝗘𝗫𝗔𝗠𝗣𝗟𝗘</b></blockquote>

<pre><code>curl -L "{Config.API_DOMAIN}/stream/VIDEO_ID?key=YOUR_API_KEY&amp;type=audio" -o song.mp3</code></pre>"""

# ============================================================
# START
# ============================================================

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    user = await create_user(
        message.from_user.id,
        message.from_user.first_name or "User",
    )

    await message.reply_text(
        format_home(user),
        reply_markup=main_keyboard(),
        disable_web_page_preview=True,
    )


# ============================================================
# CALLBACKS
# ============================================================

@app.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    user = await get_user(user_id)

    if not user:
        user = await create_user(
            user_id,
            query.from_user.first_name or "User",
        )

    data = query.data

    try:
        if data == "home":
            await query.message.edit_text(
                format_home(user),
                reply_markup=main_keyboard(),
                disable_web_page_preview=True,
            )

        elif data == "get_key":
            await query.message.edit_text(
                format_key(user),
                reply_markup=key_keyboard(),
                disable_web_page_preview=True,
            )

        elif data == "regenerate":
            user = await regenerate_key(user_id)
            await query.message.edit_text(
                "⚡ <b>API KEY REGENERATED!</b>\n\n" + format_key(user),
                reply_markup=key_keyboard(),
                disable_web_page_preview=True,
            )

        elif data == "status":
            await query.message.edit_text(
                format_status(),
                reply_markup=status_keyboard(),
                disable_web_page_preview=True,
            )

        elif data == "docs":
            await query.message.edit_text(
                format_docs(),
                reply_markup=docs_keyboard(),
                disable_web_page_preview=True,
            )

        elif data == "python_example":
            await query.message.edit_text(
                format_python(),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ 𝗗𝗢𝗖𝗦", callback_data="docs")],
                    [InlineKeyboardButton("🏠 𝗛𝗢𝗠𝗘", callback_data="home")],
                ]),
                disable_web_page_preview=True,
            )

        elif data == "curl_example":
            await query.message.edit_text(
                format_curl(),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ 𝗗𝗢𝗖𝗦", callback_data="docs")],
                    [InlineKeyboardButton("🏠 𝗛𝗢𝗠𝗘", callback_data="home")],
                ]),
                disable_web_page_preview=True,
            )

        await query.answer()

    except Exception as e:
        print(f"Callback error [{data}]: {e}")
        try:
            await query.answer("Something went wrong. Please try again.", show_alert=True)
        except Exception:
            pass


# ============================================================
# OPTIONAL ADMIN COMMAND
# ============================================================

@app.on_message(filters.command("user") & filters.private)
async def user_info(client: Client, message: Message):
    if Config.OWNER_ID and message.from_user.id != Config.OWNER_ID:
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) != 2 or not parts[1].isdigit():
        await message.reply_text("Usage: <code>/user 123456789</code>")
        return

    target = await get_user(int(parts[1]))
    if not target:
        await message.reply_text("User not found.")
        return

    await message.reply_text(
        f"""<b>USER INFO</b>

ID: <code>{target['user_id']}</code>
Name: {target.get('first_name', 'User')}
Key: <code>{target['api_key']}</code>
Tier: {target.get('tier')}
Status: {target.get('status')}
Today: {target.get('requests_today', 0)}
Total: {target.get('total_requests', 0)}
Data: {target.get('data_streamed', 0)} B"""
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    print("🚀 kirti API Bot starting...")
    app.run()
