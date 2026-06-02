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
    save_message,
    save_memory,
    get_memory,
    get_summary
)

from ai import chat_with_ai


async def ping(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != OWNER_ID:
        return

    await update.message.reply_text("pong")


async def setproject(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != OWNER_ID:
        return

    project_text = update.message.text.replace(
        "/setproject",
        "",
        1
    ).strip()

    if not project_text:
        await update.message.reply_text(
            "Format: /setproject deskripsi project"
        )
        return

    save_memory(
        "project_memory",
        project_text
    )

    await update.message.reply_text(
        "Project memory updated."
    )


async def project(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != OWNER_ID:
        return

    project_text = get_memory(
        "project_memory"
    )

    if not project_text:
        project_text = "Belum ada project memory."

    await update.message.reply_text(
        project_text
    )


async def memory(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != OWNER_ID:
        return

    project_text = get_memory(
        "project_memory"
    )

    if not project_text:
        project_text = "Belum ada project memory."

    summary = get_summary()

    if not summary:
        summary = "Belum ada summary."

    await update.message.reply_text(
        f"PROJECT MEMORY:\n\n{project_text}\n\nSUMMARY:\n\n{summary}"
    )


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
    CommandHandler("setproject", setproject)
)

app.add_handler(
    CommandHandler("project", project)
)

app.add_handler(
    CommandHandler("memory", memory)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        chat
    )
)

print("Telegram bot running...")

app.run_polling()
