from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config import TELEGRAM_TOKEN, OWNER_ID
from memory import (
    init_db,
    save_memory,
    get_memory
)


async def ping(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != OWNER_ID:
        return

    await update.message.reply_text("pong")


async def remember(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != OWNER_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Format: /remember key value"
        )
        return

    key = context.args[0]
    value = " ".join(context.args[1:])

    save_memory(key, value)

    await update.message.reply_text(
        f"Saved: {key} = {value}"
    )


async def recall(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != OWNER_ID:
        return

    if len(context.args) < 1:
        await update.message.reply_text(
            "Format: /recall key"
        )
        return

    key = context.args[0]

    value = get_memory(key)

    if value:
        await update.message.reply_text(
            f"{key} = {value}"
        )
    else:
        await update.message.reply_text(
            "Memory not found"
        )


init_db()

app = Application.builder().token(
    TELEGRAM_TOKEN
).build()

app.add_handler(
    CommandHandler("ping", ping)
)

app.add_handler(
    CommandHandler("remember", remember)
)

app.add_handler(
    CommandHandler("recall", recall)
)

print("Telegram bot running...")

app.run_polling()
