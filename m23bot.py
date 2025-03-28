import logging
import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Get bot token from GitHub Secrets
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing. Make sure it's set in GitHub Secrets.")

# GitHub releases page URL
GITHUB_RELEASES_URL = "https://github.com/Aflaungos/UpdateNotifierBot/releases"
# Version URLs for m23 and f23
M23_VERSION_URL = "https://github.com/Aflaungos/UpdateNotifierBot/blob/master/LatestVersion_SM-M236B"
F23_VERSION_URL = "https://github.com/Aflaungos/UpdateNotifierBot/blob/master/LatestVersion_SM-E236B"

# Logging setup
logging.basicConfig(level=logging.INFO)

# Command handler for m23version
async def m23version(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"The current M23 version is available here: {M23_VERSION_URL}")

# Command handler for f23version
async def f23version(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"The current F23 version is available here: {F23_VERSION_URL}")

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
