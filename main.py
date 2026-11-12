import asyncio, os
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SESSION = os.getenv("SESSION", "")

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
pytgcalls = PyTgCalls(userbot)

@app.on_message(filters.command("start"))
async def start(_, m: Message):
    await m.reply_text("Bot Chal Gaya!")

@app.on_message(filters.command("skip"))
async def skip(_, m: Message):
    try:
        await pytgcalls.leave_group_call(m.chat.id)
        await m.reply_text("Skipped!")
    except Exception as e:
        await m.reply_text(f"Error: {e}")

async def main():
    await app.start()
    await userbot.start()
    await pytgcalls.start()
    print("Bot Started!")
    await asyncio.Event().wait()

asyncio.run(main())
