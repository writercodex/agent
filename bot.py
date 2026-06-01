from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config import TELEGRAM_TOKEN


async def ping(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text("pong")


app = Application.builder().token(
    TELEGRAM_TOKEN
).build()

app.add_handler(
    CommandHandler("ping", ping)
)

print("Telegram bot running...")

app.run_polling()
