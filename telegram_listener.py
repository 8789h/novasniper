import os
import re
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events

# === Load environment variables ===
load_dotenv()
api_id_str = os.getenv("TELEGRAM_API_ID")
if not api_id_str:
    raise ValueError("TELEGRAM_API_ID is missing from environment variables")
api_id = int(api_id_str)
api_hash = os.getenv("TELEGRAM_API_HASH")
session_name = "session.session"  # Use pre-authenticated session file
channel_id = int(os.getenv("TELEGRAM_CHANNEL_ID"))

# === Regex: full pump.fun links or raw tokens ending in 'pump'
TOKEN_REGEX = re.compile(r'(?:https://pump\.fun/)?([A-Za-z0-9]{32,}pump)')

# === Extract token label from messages like "$cat", "$IMAGINE"
LABEL_REGEX = re.compile(r'\$(\w+)', re.IGNORECASE)

# === Start the Telegram listener ===
async def start_telegram_listener(callback):
    client = TelegramClient(session_name, api_id, api_hash)

    @client.on(events.NewMessage(chats=channel_id))
    async def handler(event):
        text = event.raw_text.strip()
        print(f"📨 Incoming: {text}")

        token_match = TOKEN_REGEX.search(text)
        label_match = LABEL_REGEX.search(text)

        if token_match:
            token_address = token_match.group(1)
            token_label = label_match.group(1).upper() if label_match else "TOKEN"

            print(f"🎯 Detected token: {token_address}")
            callback(token_address, token_label)

    await client.connect()
    if not await client.is_user_authorized():
        raise Exception("❌ Telegram client not authorized. Upload your session.session file.")
    
    print("🤖 Telegram client started.")
    await client.run_until_disconnected()


