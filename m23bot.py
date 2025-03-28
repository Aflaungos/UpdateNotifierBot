import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = "7743466912:AAElEgA_dyxmOSfwp8a2dfbrFmVyYpAyrW8"

# GitHub raw URLs
URLS = {
    "m23version": "https://raw.githubusercontent.com/Aflaungos/UpdateNotifierBot/master/LatestVersion_SM-M236B",
    "f23version": "https://raw.githubusercontent.com/Aflaungos/UpdateNotifierBot/master/LatestVersion_SM-E236B",
}

# Fetch version from GitHub
def get_version(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        logging.error(f"Error fetching version: {e}")
        return "Failed to fetch version."

# Command handler
def version_command(update: Update, context: CallbackContext):
    command = update.message.text.lstrip("/")
    if command in URLS:
        version = get_version(URLS[command])
        update.message.reply_text(f"Latest {command.upper()} version: {version}")
    else:
        update.message.reply_text("Invalid command. Use /m23version or /f23version.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler(["m23version", "f23version"], version_command))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
