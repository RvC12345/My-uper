import requests
import os,time
from datetime import timedelta
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
from text import Start,Help,Commands
from config import Config

# Replace these with your own bot credentials
API_ID = Config.API_ID #os.environ.get("apiid")
API_HASH = Config.API_HASH #os.environ.get("apihash")
BOT_TOKEN = Config.BOT_TOKEN #os.environ.get("tk")
#AuthU=int(os.environ.get("auth"))
AuthU = Config.AUTH_USERS #list(map(int, os.environ.get("auth").split(',')))

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN,workers=10,plugins=dict(root="plugin"))

# Run the bot
app.run()
