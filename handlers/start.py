import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

import database as db
from config import CHANNEL_ID
from messages import WELCOME_NOT_SUBSCRIBED, NOT_SUBSCRIBED_AGAIN, TRAINER_MSG

logger = logging.getLogger(__name__)


async def _check_subscription(bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status not in ("left", "kicked", "banned")
    except Exception as e:
        logger.warning("get_chat_member failed (is bot admin of %s?): %s", CHANNEL_ID, e)
        return True


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await db.add_user(user.id, user.username or "", user.first_name or "", user.last_name or "")

    subscribed = await _check_subscription(context.bot, user.id)
    if not subscribed:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("I've subscribed ✓", callback_data="check_sub")],
        ])
        await update.message.reply_text(WELCOME_NOT_SUBSCRIBED, reply_markup=keyboard)
    else:
        await db.set_subscribed_at(user.id)
        await update.message.reply_text(TRAINER_MSG)


async def cb_check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    subscribed = await _check_subscription(context.bot, user.id)
    if not subscribed:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("I've subscribed ✓", callback_data="check_sub")],
        ])
        await query.edit_message_text(NOT_SUBSCRIBED_AGAIN, reply_markup=keyboard)
    else:
        await db.set_subscribed_at(user.id)
        await query.edit_message_text(TRAINER_MSG)


def build_start_handler() -> CommandHandler:
    return CommandHandler("start", cmd_start)


def register_extra(app):
    app.add_handler(CallbackQueryHandler(cb_check_sub, pattern="^check_sub$"))
