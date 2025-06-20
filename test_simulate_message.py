import asyncio
from telegram_listener import handle_message
from telethon.tl.types import Message

class FakeEvent:
    def __init__(self, text):
        self.message = Message(id=0, message=text)

async def simulate():
    msg = "🚀 New gem: https://pump.fun/4FLAxLGL8hDYanUuh3Y3c9WbSwYatCzQqM9RsmwHgSFa"
    event = FakeEvent(msg)
    await handle_message(event)

asyncio.run(simulate())

