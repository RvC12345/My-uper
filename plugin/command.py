from pyrogram import Client, filters
from text import Start, Help, Commands
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

@Client.on_message(filters.command("start"))
async def start_bot(bot, m):
  #bot.send_message(start)
  inline_keyboard=[
  InlineKeyboardButton("HELP",callback_data="HELP"),
  InlineKeyboardButton("COMMANDS",callback_data="Commands")
    ]
  reply_markup = InlineKeyboardMarkup(inline_keyboard)
  await bot.send_message(
         chat_id=m.chat.id,
         text=Start,
         reply_markup=reply_markup,
         #reply_to_message_id=update.id
          )

