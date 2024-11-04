import time
import requests
from pyrogram import Client, filters
from seedrcc import Seedr
from pyrogram.types import Message
from config import Config

# Seedr and Telegram Bot credentials
SEEDR_USERNAME = Config.seedr_un
SEEDR_PASSWORD = Config.seedr_pw

# Initialize Seedr client and Pyrogram bot client
seedr = Seedr(SEEDR_USERNAME, SEEDR_PASSWORD)

def download_file(file_url, file_name, message):
    response = requests.get(file_url, stream=True)
    with open(file_name, "wb") as f:
        total_length = int(response.headers.get('content-length'))
        downloaded = 0
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                progress = (downloaded / total_length) * 100
                client.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    text=f"Downloading: {progress:.2f}%"
                )
    return file_name


@client.on_message(filters.regex(pattern=".*magnet.*"))
async def download_magnet(client, message):
    magnet_link = message.text
    rpm = await message.reply_text("Adding magnet link to Seedr...")
    # Step 1: Add Magnet Link to Seedr
    folder = seedr.add_folder(magnet_link)
    if not folder:
        await rpm.edit_text("Failed to add magnet link. Please check and try again.")
        return

    folder_id = folder['id']
    await rpm.edit_text("Magnet link added. Waiting for Seedr to complete the download...")

    # Step 2: Monitor Download Progress on Seedr
    while True:
        folder_status = seedr.get_folder(folder_id)
        if folder_status and folder_status["size"] > 0:
            await rpm.edit_text("Download on Seedr completed. Starting download to server...")
            break
        time.sleep(10)

    # Step 3: Download File to Server
    file_info = folder_status["files"][0]  # Only handling the first file here
    file_url = file_info["url"]
    file_name = file_info["name"]

    downloaded_file = download_file(file_url, file_name, message)

    # Step 4: Send File to User
    await rpm.edit_text("Uploading file to Telegram...")
    await client.send_document(
        chat_id=message.chat.id,
        document=downloaded_file,
        caption="Here is your downloaded file!"
    )

    # Step 5: Delete Folder and Files from Seedr
    seedr.delete_folder(folder_id)
    await rpm.edit_text("File deleted from Seedr.")

