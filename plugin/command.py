from pyrogram import Client, filters
from text import Start, Help, Commands

@Client.on_message(filters.command("start") & filters.private,)
async def start_bot(bot, m: Message):
  bot.reply(start)
