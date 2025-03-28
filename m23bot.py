import logging
import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Get bot token from GitHub Secrets
TOKEN = os.getenv("BOT_TOKEN")

# Check if the token exists
if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing. Make sure it's set in GitHub Secrets.")

# GitHub raw URLs
URLS = {
    "m23version": "https://raw.githubusercontent.com/Aflaungos/UpdateNotifierBot/master/LatestVersion_SM-M236B",
    "f23version": "https://raw.githubusercontent.com/Aflaungos/UpdateNotifierBot/master/LatestVersion_SM-E236B",
}

# Fetch version from GitHub
async def get_version(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        logging.error(f"Error fetching version: {e}")
        return "Failed to fetch version."

# Command handler
async def version_command(update: Update, context: CallbackContext):
    command = update.message.text.lstrip("/")
    if command in URLS:
        version = await get_version(URLS[command])
        await update.message.reply_text(f"Latest {command.upper()} version: {version}")
    else:
        await update.message.reply_text("Invalid command. Use /m23version or /f23version.")

def main():
    # Initialize the bot application
    app = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("m23version", version_command))
    app.add_handler(CommandHandler("f23version", version_command))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
