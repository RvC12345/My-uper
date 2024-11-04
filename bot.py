import requests
import time
from datetime import timedelta
from pyrogram import Client, filters
from pyrogram.types import Message

# Replace these with your own bot credentials
API_ID = os.environ.get("apiid")
API_HASH = os.environ.get("apihash")
BOT_TOKEN = os.environ.get("tk")
AuthU=int(os.environ.get("auth"))

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Progress bar function to create visual progress with 10 blocks
def create_progress_bar(progress):
    num_blocks = 10
    completed_blocks = progress // (100 // num_blocks)
    bar = '✅️' * completed_blocks + '❌️' * (num_blocks - completed_blocks)
    return bar

# Function to download file with progress update
def download_file(url, output_path, message: Message):
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
                    message_text = f"[{bar}]\nPercentage: {progress}%\nETA: {eta_formatted}"
                    app.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_text)

# Function to upload file with progress update
async def upload_file(client, message, file_path):
    file_size = message.reply_to_message.document.file_size if message.reply_to_message.document else 0
    uploaded = 0
    start_time = time.time()

    def progress(current, total):
        nonlocal uploaded
        uploaded = current
        
        # Calculate upload progress
        progress = int((uploaded / total) * 100)
        bar = create_progress_bar(progress)
        
        # Calculate ETA
        elapsed_time = time.time() - start_time
        eta = (elapsed_time / uploaded) * (total - uploaded) if uploaded > 0 else 0
        eta_formatted = str(timedelta(seconds=int(eta)))

        # Update message with upload progress
        message_text = f"[{bar}]\nPercentage: {progress}%\nETA: {eta_formatted}"
        client.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_text)

    # Send the file with progress callback
    await client.send_document(
        chat_id=message.chat.id,
        document=file_path,
        progress=progress,
    )

# Command handler to start URL download and upload
@app.on_message(filters.command("upload"))
async def url_upload_handler(client, message):
    # Extract URL from the message text
    url = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
    if not url:
        await message.reply("Please provide a URL to upload.")
        return

    # Temporary file path
    output_path = "downloaded_file"

    # Initial message
    progress_message = await message.reply("Starting download...")

    # Download the file
    download_file(url, output_path, progress_message)

    # Upload the file
    await progress_message.edit_text("Download complete. Starting upload...")
    await upload_file(client, progress_message, output_path)

    # Cleanup: Delete the local file after upload
    os.remove(output_path)
    await progress_message.edit_text("Upload complete!")

# Run the bot
app.run()
