from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler,
    CallbackQueryHandler, MessageHandler, CommandHandler, filters,
)

import database as db
from messages import KEV_ASK_NAME, KEV_ASK_PHONE, KEV_SUCCESS, KEV_ALREADY

ASK_NAME, ASK_PHONE = range(2)


async def kev_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if await db.is_kev_registered(user_id):
        await query.message.reply_text(KEV_ALREADY, parse_mode="Markdown")
        return ConversationHandler.END

    await query.message.reply_text(KEV_ASK_NAME, parse_mode="Markdown")
    return ASK_NAME


async def got_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["kev_name"] = update.message.text.strip()
    await update.message.reply_text(KEV_ASK_PHONE, parse_mode="Markdown")
    return ASK_PHONE


async def got_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    name = context.user_data.get("kev_name", user.full_name)
    phone = update.message.text.strip()

    await db.register_kev(user.id, name, phone)
    await update.message.reply_text(KEV_SUCCESS, parse_mode="Markdown")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Registration cancelled. Type /start to begin again.")
    return ConversationHandler.END


def build_kev_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(kev_entry, pattern="^kev_start$")],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, got_name)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, got_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", cancel)],
        per_message=False,
    )
