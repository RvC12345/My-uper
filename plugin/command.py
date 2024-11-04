from pyrogram import Client, filters
from text import Start, Help, Commands
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

def Btn(t,data=""):
  return InlineKeyboardButton(t,callback_data=data)

@Client.on_message(filters.command("start"))
async def start_bot(bot, m):
  #bot.send_message(start)
  inline_keyboard=[
        [
    InlineKeyboardButton("HELP",callback_data="help"),
    InlineKeyboardButton("COMMANDS",callback_data="commands")
        ]
    ]
  reply_markup = InlineKeyboardMarkup(inline_keyboard)
  await bot.send_message(
         chat_id=m.chat.id,
         text=Start,
         reply_markup=reply_markup,
         #reply_to_message_id=update.id
          )

@Client.on_callback_query()
async def _clback(bot,update):
  if update.data == "help":
     update.message.edit(
       text=Help,
       reply_markup=InlineKeyboardMarkup([[Btn("Back",data="home")]])
     )
  elif update.data == "commands":
    update.message.edit(
       text=Commands,
       reply_markup=InlineKeyboardMarkup([[Btn("Back",data="home")]])
    )
  elif update.data == "home":
    update.message.edit(
       text=Start,
       reply_markup=InlineKeyboardMarkup([[Btn("HELP",data="help"),Btn("COMMANDS",data="commands")]])
    )
