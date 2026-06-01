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
    get_memory
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


async def chat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != OWNER_ID:
        return

    user_message = update.message.text

    save_message(
        "user
