import logging
import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Get bot token from GitHub Secrets
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing. Make sure it's set in GitHub Secrets.")

# GitHub raw URLs
URLS = {
    "m23version": "https://raw.githubusercontent.com/Aflaungos/UpdateNotifierBot/master/LatestVersion_SM-M236B",
    "f23version": "https://raw.githubusercontent.com/Aflaungos/UpdateNotifierBot/master/LatestVersion_SM-E236B",
}

# GitHub releases API URL
GITHUB_RELEASES_URL = "https://api.github.com/repos/Aflaungos/UpdateNotifierBot/releases/latest"

# Logging setup
logging.basicConfig(level=logging.INFO)

# Fetch version from GitHub
async def get_version(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        logging.error(f"Error fetching version: {e}")
        return "Failed to fetch version."

# Command handler for version fetching
async def version_command(update: Update, context: CallbackContext):
    command = update.message.text.lstrip("/")
    if command in URLS:
        version = await get_version(URLS[command])
        await update.message.reply_text(f"Latest {command.upper()} version: {version}")
    else:
        await update.message.reply_text("Invalid command. Use /m23version or /f23version.")

# Command handler to download firmware files
async def download_firmware(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    # Inform user about the firmware location
    await update.message.reply_text(f"Firmware downloads available here:\n🔗 [GitHub Releases](https://github.com/Aflaungos/UpdateNotifierBot/releases)")

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

        for asset in assets:
            file_url = asset["browser_download_url"]
            file_name = asset["name"]

            # Download the file
            file_path = f"/tmp/{file_name}"  # Temporary storage
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
    app.add_handler(CommandHandler("m23version", version_command))
    app.add_handler(CommandHandler("f23version", version_command))
    app.add_handler(CommandHandler("downloadfirmware", download_firmware))  # New command

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
