from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

from config import TELEGRAM_TOKEN, OWNER_ID

from memory import (
    init_db,
    save_message
)

from ai import chat_with_ai


async def ping(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != OWNER_ID:
        return

    await update.message.reply_text("pong")


async def chat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != OWNER_ID:
        return

    user_message = update.message.text

    save_message(
        "user",
        user_message
    )

    reply = chat_with_ai(
        user_message
    )

    save_message(
        "assistant",
        reply
    )

    await update.message.reply_text(
        reply
    )


init_db()

app = Application.builder().token(
    TELEGRAM_TOKEN
).build()

app.add_handler(
    CommandHandler("ping", ping)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        chat
    )
)

print("Telegram bot running...")

app.run_polling()
