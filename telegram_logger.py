import logging
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

FLUENTD_ENDPOINT = os.getenv("FLUENTD_ENDPOINT")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Надішли мені повідомлення, я його залогую 📝")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text

    log_data = {
        "@timestamp": datetime.utcnow().isoformat() + "Z",
        "type": "telegram_message",
        "user_id": user.id,
        "username": user.username,
        "message": message_text
    }

    try:
        response = requests.post(FLUENTD_ENDPOINT, json=log_data)
        response.raise_for_status()
        print("✅ Log sent to Fluentd:", log_data)
    except Exception as e:
        print("❌ Error sending log to Fluentd:", e)

    await update.message.reply_text("✅ Повідомлення надіслано в систему логування!")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущено.")
    app.run_polling()

