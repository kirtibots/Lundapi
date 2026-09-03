# KIRTI API Telegram Bot

A Pyrogram + MongoDB Telegram API-key management bot.

## Features

- `/start` welcome UI
- Per-user API key generation
- Regenerate API key
- Quota and usage screen
- API status screen
- API documentation
- Python and CURL examples
- MongoDB persistence
- Premium styled Telegram UI
- Heroku worker configuration

## Heroku deployment

Create a Heroku app and add these Config Vars:

```text
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_bot_token
MONGO_URL=your_mongodb_connection_string
DB_NAME=kirti_api
OWNER_ID=your_telegram_numeric_id
UPDATES_URL=https://t.me/your_updates
SUPPORT_URL=https://t.me/your_support
API_NAME=KIRTI API
API_DOMAIN=https://your-api-domain.example
DAILY_LIMIT=6000
TIER=FREE
```

Then deploy this ZIP/repository. Heroku will use:

```text
worker: python bot.py
```

After deployment, scale the worker to 1 dyno.

## Local

```bash
pip install -r requirements.txt
python bot.py
```

Rename `.env.example` to `.env` for local use.

## Important

`API_DOMAIN` is only the URL displayed in the bot's documentation. This package does not itself implement an audio/video streaming backend. Point it to your own API server.
