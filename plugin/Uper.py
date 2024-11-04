from pyrogram import Client, filters
from text import Start, Help, Commands
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
import asyncio
import requests
import os,time,filetype
from datetime import timedelta
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from urllib.parse import urlparse
from config import Config

AuthU = Config.AUTH_USERS

# Progress bar function to create visual progress with 10 blocks
def create_progress_bar(progress):
    num_blocks = 10
    completed_blocks = progress // (100 // num_blocks)
    bar = '✅️' * completed_blocks + '❌️' * (num_blocks - completed_blocks)
    return bar

# Function to download file with progress update
def download_file(client, url, output_path, message):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    start_time = time.time()
    last_update = 0

    with open(output_path, 'wb') as file:
        for chunk in response.iter_content(1024):  # 1 KB chunks
            if chunk:
                file.write(chunk)
                downloaded += len(chunk)

                # Calculate download progress
                progress = int((downloaded / total_size) * 100)
                
                # Update message at every 10%
                if progress >= last_update + 10:
                    last_update = progress // 10 * 10  # Round to the nearest 10%
                    bar = create_progress_bar(progress)
                    
                    # Calculate ETA
                    elapsed_time = time.time() - start_time
                    eta = (elapsed_time / downloaded) * (total_size - downloaded) if downloaded > 0 else 0
                    eta_formatted = str(timedelta(seconds=int(eta)))

                    # Update message with download progress
                    message_text = f"🔰Downloading...📥\n\n [{bar}]\n\n➡️Percentage: {progress}%\n➡️ETA: {eta_formatted}"
                    asyncio.run_coroutine_threadsafe(
                        client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=message_text),
                        client.loop
                    )

# Function to upload file with progress update
async def upload_file(client, message, file_path):
    #file_size = message.reply_to_message.document.file_size if message.reply_to_message.document else 0
    uploaded = 0
    start_time = time.time()
    last_update = 0
    if "?" in file_path:
        file_path = file_path.split("?")[0]
    #filetype=file_path.split(".")[1]  
    file_name=file_path.split(".")[0]
    def progress(current, total):
        nonlocal uploaded
        nonlocal last_update
        uploaded = current
        
        # Calculate upload progress
        progress = int((uploaded / total) * 100)
        if progress >= last_update + 10:
           last_update = progress // 10 * 10  # Round to the nearest 10%
           bar = create_progress_bar(progress)
        
        # Calculate ETA
           elapsed_time = time.time() - start_time
           eta = (elapsed_time / uploaded) * (total - uploaded) if uploaded > 0 else 0
           eta_formatted = str(timedelta(seconds=int(eta)))

        # Update message with upload progress
           message_text = f"**🔰Uploading...🚀**\n\n [{bar}]\n\n➡️Percentage: {progress}%\n➡️ETA: {eta_formatted}"
           client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=message_text)
  
    # Send the file with progress callback
    try:
       file = filetype.guess(file_path)
       xfiletype = file.mime
    except AttributeError:
       xfiletype = file_name
       print("Err on Making file name")
    if xfiletype in ['video/mp4', 'video/x-matroska', 'video/webm']:
        metadata = extractMetadata(createParser(file_path))
        if metadata is not None:
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
                await client.send_video(
                    chat_id=message.chat.id,
                    video=file_path,
                    caption=file_name,
                    duration=duration,
                    progress=progress,
                  )
    else:
        await client.send_document(
           chat_id=message.chat.id,
           document=file_path,
           progress=progress,
       )

# Command handler to start URL download and upload
@Client.on_message(filters.regex(pattern=".*http.*"))
async def url_upload_handler(client, message):
    # Extract URL from the message text
  if message.chat.id not in AuthU:
    await message.reply("You are not my auther")
  else:
    url = message.text #.split(" ", 1)[1] if len(message.text.split()) > 1 else None
    if not url:
        await message.reply("Please provide a URL to upload.")
        return 
    # Temporary file path
    output_path = urlparse(url).path.split('/')[-1]


    # Initial message
    progress_message = await message.reply("**Starting download...**")

    # Download the file
    download_file(client, url, output_path, progress_message)

    # Upload the file
    await progress_message.edit_text("**Download complete.\nStarting upload...**")
    await upload_file(client, progress_message, output_path)

    # Cleanup: Delete the local file after upload
    os.remove(output_path)
    await progress_message.edit_text("**Upload complete!**")

