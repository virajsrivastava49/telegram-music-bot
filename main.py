import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped, StreamType

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
SESSION = os.environ.get("SESSION", "")

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client(SESSION, api_id=API_ID, api_hash=API_HASH)
pytgcalls = PyTgCalls(userbot)

@app.on_message(filters.command("start"))
async def start(_, m: Message):
    await m.reply_text("Hi! Main Music Bot hu.\nGroup me mujhe add karo, fir /play <gaane ka naam> likho.")

@app.on_message(filters.command("play") & filters.group)
async def play(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("Use karo: /play arijit singh tum hi ho")
    query = " ".join(m.command[1:])
    await m.reply_text(f"Searching: {query}\n\nNote: Pehle assistant ko group me add karo aur voice chat start karo.")
    try:
        await pytgcalls.join_group_call(
            m.chat.id,
            AudioPiped(f"https://www.youtube.com/results?search_query={query}", audio_parameters=None),
            stream_type=StreamType().pulse_stream,
        )
        await m.reply_text("Playing... /stop se band karo")
    except Exception as e:
        await m.reply_text(f"Error: {e}\nVoice chat on hai? Assistant group me hai?")

@app.on_message(filters.command(["stop", "end"]))
async def stop(_, m: Message):
    try:
        await pytgcalls.leave_group_call(m.chat.id)
        await m.reply_text("Music band kar diya.")
    except Exception as e:
        await m.reply_text(f"Error: {e}")

@app.on_message(filters.command("skip"))
async def skip(_, m: Message):
    await m.reply_text("Skip feature is version me nahi hai, /stop karke naya /play karo.")

async def main():
    await app.start()
    await userbot.start()
    await pytgcalls.start()
    print("Bot Started!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
