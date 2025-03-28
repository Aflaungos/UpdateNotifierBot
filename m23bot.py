import logging
import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Get bot token from GitHub Secrets
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing. Make sure it's set in GitHub Secrets.")

# GitHub releases API URL
GITHUB_RELEASES_URL = "https://api.github.com/repos/Aflaungos/UpdateNotifierBot/releases/latest"

# Logging setup
logging.basicConfig(level=logging.INFO)

# Command handler to download only kernel.tar.md5 and PIT files
async def download_firmware(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    await update.message.reply_text("📦 Fetching Kernel and PIT files...")

    try:
        # Fetch latest release data
        response = requests.get(GITHUB_RELEASES_URL)
        response.raise_for_status()
        release_data = response.json()

        # Extract asset download URLs
        assets = release_data.get("assets", [])
        if not assets:
            await update.message.reply_text("⚠️ No firmware files found in the latest release.")
            return

        # Filter only Kernel TAR and PIT files
        firmware_files = [asset for asset in assets if asset["name"].endswith((".tar.md5", ".pit"))]

        if not firmware_files:
            await update.message.reply_text("⚠️ Kernel or PIT files not found in the latest release.")
            return

        for asset in firmware_files:
            file_url = asset["browser_download_url"]
            file_name = asset["name"]

            # Download the file
            file_path = f"/tmp/{file_name}"
            with requests.get(file_url, stream=True) as r:
                r.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            # Send the file to Telegram
            with open(file_path, "rb") as f:
                await context.bot.send_document(chat_id, document=f, filename=file_name)

            logging.info(f"Sent {file_name} to chat {chat_id}")

    except requests.RequestException as e:
        logging.error(f"Error fetching firmware: {e}")
        await update.message.reply_text("⚠️ Failed to fetch firmware files.")

# Main function to start the bot
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("downloadfirmware", download_firmware))  # Fixed command

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
