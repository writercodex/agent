from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config import TELEGRAM_TOKEN, OWNER_ID


async def ping(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != OWNER_ID:
        return

    await update.message.reply_text("pong")


app = Application.builder().token(
    TELEGRAM_TOKEN
).build()

app.add_handler(
    CommandHandler("ping", ping)
)

print("Telegram bot running...")

app.run_polling()
