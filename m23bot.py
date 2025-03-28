import logging
import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Get bot token from GitHub Secrets
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing. Make sure it's set in GitHub Secrets.")

# GitHub raw URLs for version files
M23_VERSION_URL = "https://raw.githubusercontent.com/Aflaungos/UpdateNotifierBot/master/LatestVersion_SM-M236B"
F23_VERSION_URL = "https://raw.githubusercontent.com/Aflaungos/UpdateNotifierBot/master/LatestVersion_SM-E236B"

# Logging setup
logging.basicConfig(level=logging.INFO)

# Function to fetch and parse version file
def fetch_version(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        version_text = response.text.strip()
        # Extract the part before the first '/'
        version = version_text.split('/')[0] if '/' in version_text else version_text
        return version
    except requests.RequestException as e:
        logging.error(f"Error fetching version: {e}")
        return "⚠️ Failed to fetch version."

# Command handler for m23version
async def m23version(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    version = fetch_version(M23_VERSION_URL)
    await update.message.reply_text(f"The current M23 version is: {version}")

# Command handler for f23version
async def f23version(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    version = fetch_version(F23_VERSION_URL)
    await update.message.reply_text(f"The current F23 version is: {version}")

# Command handler for downloadfirmware (sending releases link)
async def download_firmware(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"📦 You can download the latest firmware from here:\n🔗 [GitHub Releases](https://github.com/Aflaungos/UpdateNotifierBot/releases)", parse_mode="Markdown")

# Main function to start the bot
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("m23version", m23version))  # Command for m23 version
    app.add_handler(CommandHandler("f23version", f23version))  # Command for f23 version
    app.add_handler(CommandHandler("downloadfirmware", download_firmware))  # Command for downloading firmware

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
