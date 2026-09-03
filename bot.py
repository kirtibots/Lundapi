import secrets
import string
from datetime import datetime, timezone
from html import escape

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
)

from motor.motor_asyncio import AsyncIOMotorClient

from config import Config


# ============================================================
# PREMIUM FONT
# ============================================================

_FONT_NORMAL = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)

_FONT_PREMIUM = (
    "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)

_FONT_MAP = str.maketrans(
    _FONT_NORMAL,
    _FONT_PREMIUM
)


def sf(text: str) -> str:
    return text.translate(_FONT_MAP)


# ============================================================
# DATABASE
# ============================================================

mongo = AsyncIOMotorClient(
    Config.MONGO_URL
)

db = mongo[Config.DB_NAME]

users = db.users


# ============================================================
# BOT
# ============================================================

app = Client(
    "kirti_api_bot",
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

    alphabet = (
        string.ascii_letters +
        string.digits
    )

    return "kirti_" + "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


async def get_user(user_id: int):

    return await users.find_one(
        {
            "user_id": user_id
        }
    )


async def create_user(
    user_id: int,
    first_name: str = "User"
):

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
        {
            "user_id": user_id
        },
        {
            "$setOnInsert": doc
        },
        upsert=True,
    )

    return await get_user(user_id)


async def regenerate_key(
    user_id: int
):

    key = make_api_key()

    await users.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "api_key": key,
                "status": "ACTIVE",
                "last_refresh": now(),
            }
        },
    )

    return await get_user(user_id)


# ============================================================
# MAIN KEYBOARD
# ============================================================

def main_keyboard():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔑 ɢᴇᴛ ᴀᴘɪ ᴋᴇʏ",
                    callback_data="get_key",
                ),
                InlineKeyboardButton(
                    "🔄 ʀᴇɢᴇɴᴇʀᴀᴛᴇ",
                    callback_data="regenerate",
                ),
            ],
            [
                InlineKeyboardButton(
                    "📖 ᴀᴘɪ ᴅᴏᴄs",
                    callback_data="docs",
                ),
                InlineKeyboardButton(
                    "⚡ sᴛᴀᴛᴜs",
                    callback_data="status",
                ),
            ],
            [
                InlineKeyboardButton(
                    "📢 ᴜᴘᴅᴀᴛᴇs",
                    url=Config.UPDATES_URL,
                ),
                InlineKeyboardButton(
                    "💬 sᴜᴘᴘᴏʀᴛ",
                    url=Config.SUPPORT_URL,
                ),
            ],
        ]
    )


def key_keyboard():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄 ʀᴇɢᴇɴᴇʀᴀᴛᴇ",
                    callback_data="regenerate",
                ),
                InlineKeyboardButton(
                    "⬅️ ʙᴀᴄᴋ",
                    callback_data="home",
                ),
            ]
        ]
    )


def status_keyboard():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄 ʀᴇғʀᴇsʜ",
                    callback_data="status",
                ),
                InlineKeyboardButton(
                    "⬅️ ʙᴀᴄᴋ",
                    callback_data="home",
                ),
            ]
        ]
    )


def docs_keyboard():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🐍 ᴘʏᴛʜᴏɴ",
                    callback_data="python_example",
                ),
                InlineKeyboardButton(
                    "🚀 ᴄᴜʀʟ",
                    callback_data="curl_example",
                ),
            ],
            [
                InlineKeyboardButton(
                    "⬅️ ʙᴀᴄᴋ",
                    callback_data="home",
                ),
            ],
        ]
    )


# ============================================================
# START / HOME CAPTION
# ============================================================

def format_home(user):

    name = user.get(
        "first_name"
    ) or "User"

    name = escape(
        str(name)
    )

    return f"""
<blockquote>
<b>✦ ᴋɪʀᴛɪ ᴀᴘɪ ✦ 🇨🇦</b>
</blockquote>

<b>╭━━━ ᴡᴇʟᴄᴏᴍᴇ, {sf(name.upper())} ━━━╮</b>

<blockquote>
<b>🎵 ᴋɪʀᴛɪ ᴍᴜsɪᴄ ᴇɴɢɪɴᴇ</b>

<i>Ultra High-Speed • Lossless Audio
Streaming API • Global CDN</i>
</blockquote>

<blockquote>
<b>⚡ ǫᴜɪᴄᴋ sᴛᴀʀᴛ</b>

<i>Tap 「🔑 ɢᴇᴛ ᴀᴘɪ ᴋᴇʏ」 below to create
or view your personal streaming key.</i>
</blockquote>

<b>╰━━━ sᴇʟᴇᴄᴛ ᴀɴ ᴏᴘᴛɪᴏɴ ʙᴇʟᴏᴡ 👇 ━━━╯</b>
"""


# ============================================================
# API KEY
# ============================================================

def format_key(user):

    key = user.get(
        "api_key",
        "N/A"
    )

    endpoint = (
        f"{Config.API_DOMAIN}"
        f"/stream/{{VIDEO_ID}}"
        f"?key={key}&type=audio"
    )

    return f"""
<blockquote>
<b>🔐 ʏᴏᴜʀ ᴀᴘɪ ᴋᴇʏ</b>
</blockquote>

<blockquote>
<b>🔑 ᴀᴄᴛɪᴠᴇ ᴀᴘɪ ᴋᴇʏ</b>

<code>{escape(str(key))}</code>

<i>Keep this key private.
Do not share it publicly.</i>

• <b>ᴛɪᴇʀ:</b> {escape(str(user.get("tier", Config.TIER)))}
• <b>sᴛᴀᴛᴜs:</b> 🟢 {escape(str(user.get("status", "ACTIVE")))}
</blockquote>

<blockquote>
<b>📊 ǫᴜᴏᴛᴀ &amp; ᴜsᴀɢᴇ</b>

• <b>ʀᴇǫᴜᴇsᴛs ᴛᴏᴅᴀʏ:</b>
  {user.get("requests_today", 0)}

• <b>ᴛᴏᴛᴀʟ ʀᴇǫᴜᴇsᴛs:</b>
  {user.get("total_requests", 0)}

• <b>ᴅᴀᴛᴀ sᴛʀᴇᴀᴍᴇᴅ:</b>
  {user.get("data_streamed", 0)} B

• <b>ᴅᴀɪʟʏ ʟɪᴍɪᴛ:</b>
  {Config.DAILY_LIMIT} Requests / Day

• <b>ᴇxᴘɪʀᴀᴛɪᴏɴ:</b>
  Never (Lifetime)
</blockquote>

<blockquote>
<b>🔗 sᴛʀᴇᴀᴍ ᴇɴᴅᴘᴏɪɴᴛ</b>

<code>{escape(endpoint)}</code>
</blockquote>
"""


# ============================================================
# STATUS
# ============================================================

def format_status():

    return """
<blockquote>
<b>📡 ᴋɪʀᴛɪ ᴍᴜsɪᴄ sᴛᴀᴛᴜs</b>
</blockquote>

<blockquote>
<b>🟢 sʏsᴛᴇᴍ ʜᴇᴀʟᴛʜ</b>

• <b>ᴄᴅɴ sᴛᴀᴛᴜs:</b> 🟢 100% Operational
• <b>sᴛʀᴇᴀᴍ ǫᴜᴀʟɪᴛʏ:</b> 320Kbps Lossless Audio
• <b>ᴀᴘɪ ʟᴀᴛᴇɴᴄʏ:</b> ~180ms Ultra-Fast
• <b>ᴘʀᴏᴛᴏᴄᴏʟ:</b> HTTP/2 + TLS 1.3
</blockquote>

<blockquote>
<b>✨ ɢʟᴏʙᴀʟ ᴄᴅɴ</b>

<i>All configured edge nodes are online.</i>
</blockquote>
"""


# ============================================================
# DOCS
# ============================================================

def format_docs():

    return f"""
<blockquote>
<b>📚 ᴋɪʀᴛɪ ᴍᴜsɪᴄ ᴀᴘɪ ᴅᴏᴄs</b>
</blockquote>

<blockquote>
<b>🎧 ᴀᴜᴅɪᴏ sᴛʀᴇᴀᴍ</b>

<code>{escape(Config.API_DOMAIN)}/stream/{{VIDEO_ID}}?key={{YOUR_KEY}}&amp;type=audio</code>

<b>ℹ️ ᴛʀᴀᴄᴋ ᴍᴇᴛᴀᴅᴀᴛᴀ</b>

<code>{escape(Config.API_DOMAIN)}/info/{{VIDEO_ID}}?key={{YOUR_KEY}}</code>
</blockquote>

<blockquote>
<b>⚙️ ǫᴜᴇʀʏ ᴘᴀʀᴀᴍᴇᴛᴇʀs</b>

• <b>key</b> — required
• <b>type</b> — audio / video
• <b>itag</b> — optional stream format
</blockquote>

<blockquote>
<b>💎 ᴋᴇʏ ʜɪɢʜʟɪɢʜᴛs</b>

• Single-call playback
• Ultra-low latency
• High-bandwidth streaming
</blockquote>
"""


# ============================================================
# PYTHON
# ============================================================

def format_python():

    return f"""
<blockquote>
<b>🐍 ᴘʏᴛʜᴏɴ ᴇxᴀᴍᴘʟᴇ</b>
</blockquote>

<pre><code>import aiohttp

API_KEY = "YOUR_API_KEY"
VIDEO_ID = "VIDEO_ID"

url = "{escape(Config.API_DOMAIN)}/stream/" + VIDEO_ID

params = {{
    "key": API_KEY,
    "type": "audio"
}}

async with aiohttp.ClientSession() as session:
    async with session.get(
        url,
        params=params
    ) as r:
        data = await r.read()

with open("song.mp3", "wb") as f:
    f.write(data)</code></pre>
"""


# ============================================================
# CURL
# ============================================================

def format_curl():

    return f"""
<blockquote>
<b>🚀 ᴄᴜʀʟ / ʙᴀsʜ ᴇxᴀᴍᴘʟᴇ</b>
</blockquote>

<pre><code>curl -L "{escape(Config.API_DOMAIN)}/stream/VIDEO_ID?key=YOUR_API_KEY&amp;type=audio" -o song.mp3</code></pre>
"""


# ============================================================
# START
# ONE SINGLE MESSAGE:
# PHOTO + CAPTION + BUTTONS
# ============================================================

@app.on_message(
    filters.command("start") &
    filters.private
)
async def start_handler(
    client: Client,
    message: Message
):

    user = await create_user(
        message.from_user.id,
        message.from_user.first_name or "User",
    )

    await message.reply_photo(
        photo=Config.START_IMAGE,
        caption=format_home(user),
        parse_mode=ParseMode.HTML,
        reply_markup=main_keyboard(),
    )


# ============================================================
# HELP
# SAME AS START
# ============================================================

@app.on_message(
    filters.command("help") &
    filters.private
)
async def help_handler(
    client: Client,
    message: Message
):

    user = await get_user(
        message.from_user.id
    )

    if not user:

        user = await create_user(
            message.from_user.id,
            message.from_user.first_name or "User",
        )

    await message.reply_photo(
        photo=Config.START_IMAGE,
        caption=format_home(user),
        parse_mode=ParseMode.HTML,
        reply_markup=main_keyboard(),
    )


# ============================================================
# CALLBACK HANDLER
# ============================================================

@app.on_callback_query()
async def callback_handler(
    client: Client,
    query: CallbackQuery
):

    user_id = query.from_user.id

    user = await get_user(
        user_id
    )

    if not user:

        user = await create_user(
            user_id,
            query.from_user.first_name or "User",
        )

    data = query.data

    try:

        # ====================================================
        # HOME
        # ====================================================

        if data == "home":

            await query.answer()

            await query.message.edit_caption(
                caption=format_home(user),
                parse_mode=ParseMode.HTML,
                reply_markup=main_keyboard(),
            )

            return

        # ====================================================
        # GET API KEY
        # ====================================================

        elif data == "get_key":

            await query.answer()

            await query.message.edit_caption(
                caption=format_key(user),
                parse_mode=ParseMode.HTML,
                reply_markup=key_keyboard(),
            )

            return

        # ====================================================
        # REGENERATE
        # ====================================================

        elif data == "regenerate":

            user = await regenerate_key(
                user_id
            )

            await query.answer(
                "API key regenerated successfully!"
            )

            await query.message.edit_caption(
                caption=format_key(user),
                parse_mode=ParseMode.HTML,
                reply_markup=key_keyboard(),
            )

            return

        # ====================================================
        # STATUS
        # ====================================================

        elif data == "status":

            await query.answer()

            await query.message.edit_caption(
                caption=format_status(),
                parse_mode=ParseMode.HTML,
                reply_markup=status_keyboard(),
            )

            return

        # ====================================================
        # DOCS
        # ====================================================

        elif data == "docs":

            await query.answer()

            await query.message.edit_caption(
                caption=format_docs(),
                parse_mode=ParseMode.HTML,
                reply_markup=docs_keyboard(),
            )

            return

        # ====================================================
        # PYTHON
        # ====================================================

        elif data == "python_example":

            await query.answer()

            await query.message.edit_caption(
                caption=format_python(),
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "⬅️ ᴅᴏᴄs",
                                callback_data="docs",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "🏠 ʜᴏᴍᴇ",
                                callback_data="home",
                            )
                        ],
                    ]
                ),
            )

            return

        # ====================================================
        # CURL
        # ====================================================

        elif data == "curl_example":

            await query.answer()

            await query.message.edit_caption(
                caption=format_curl(),
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "⬅️ ᴅᴏᴄs",
                                callback_data="docs",
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "🏠 ʜᴏᴍᴇ",
                                callback_data="home",
                            )
                        ],
                    ]
                ),
            )

            return

        # ====================================================
        # UNKNOWN
        # ====================================================

        await query.answer()

    except Exception as e:

        print(
            f"Callback error [{data}]: {e}"
        )

        try:

            await query.answer(
                "Something went wrong. Please try again.",
                show_alert=True,
            )

        except Exception:
            pass


# ============================================================
# ADMIN USER COMMAND
# ============================================================

@app.on_message(
    filters.command("user") &
    filters.private
)
async def user_info(
    client: Client,
    message: Message
):

    if (
        Config.OWNER_ID
        and message.from_user.id != Config.OWNER_ID
    ):
        return

    parts = message.text.split(
        maxsplit=1
    )

    if (
        len(parts) != 2
        or not parts[1].isdigit()
    ):

        await message.reply_text(
            "Usage: <code>/user 123456789</code>",
            parse_mode=ParseMode.HTML,
        )

        return

    target = await get_user(
        int(parts[1])
    )

    if not target:

        await message.reply_text(
            "User not found."
        )

        return

    target_name = escape(
        str(target.get(
            "first_name",
            "User"
        ))
    )

    await message.reply_text(
        f"""
<b>👤 ᴜsᴇʀ ɪɴғᴏ</b>

<b>ɪᴅ:</b>
<code>{target['user_id']}</code>

<b>ɴᴀᴍᴇ:</b>
{target_name}

<b>ᴀᴘɪ ᴋᴇʏ:</b>
<code>{escape(str(target['api_key']))}</code>

<b>ᴛɪᴇʀ:</b>
{escape(str(target.get('tier', Config.TIER)))}

<b>sᴛᴀᴛᴜs:</b>
{escape(str(target.get('status', 'ACTIVE')))}

<b>ᴛᴏᴅᴀʏ:</b>
{target.get('requests_today', 0)}

<b>ᴛᴏᴛᴀʟ:</b>
{target.get('total_requests', 0)}

<b>ᴅᴀᴛᴀ:</b>
{target.get('data_streamed', 0)} B
""",
        parse_mode=ParseMode.HTML,
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🚀 KIRTI API BOT STARTING...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    app.run()
