import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
session_name = os.getenv("SESSION_NAME")

async def main():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()

    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        print(f"{dialog.name} → ID: {dialog.id}")

    await client.disconnect()

asyncio.run(main())

