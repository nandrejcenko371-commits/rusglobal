import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

import database as db
from config import CHANNEL_ID
from messages import WELCOME_NOT_SUBSCRIBED, NOT_SUBSCRIBED_AGAIN, TRAINER_MSG
from scheduler import send_missed_todays_broadcasts

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

    existing = await db.get_user(user.id)
    if existing and existing.get("subscribed_at"):
        # already subscribed — just resend the trainer, don't block
        await update.message.reply_text(TRAINER_MSG)
        return

    subscribed = await _check_subscription(context.bot, user.id)
    if not subscribed:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("I've subscribed ✓", callback_data="check_sub")],
        ])
        await update.message.reply_text(WELCOME_NOT_SUBSCRIBED, reply_markup=keyboard)
    else:
        await db.set_subscribed_at(user.id)
        await update.message.reply_text(TRAINER_MSG)
        await send_missed_todays_broadcasts(context.bot, user.id)


async def cb_check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    existing = await db.get_user(user.id)
    if existing and existing.get("subscribed_at"):
        return  # already got the trainer (double-tap guard)

    subscribed = await _check_subscription(context.bot, user.id)
    if not subscribed:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("I've subscribed ✓", callback_data="check_sub")],
        ])
        await query.edit_message_text(NOT_SUBSCRIBED_AGAIN, reply_markup=keyboard)
    else:
        await db.set_subscribed_at(user.id)
        await query.edit_message_text(TRAINER_MSG)
        await send_missed_todays_broadcasts(context.bot, user.id)


def build_start_handler() -> CommandHandler:
    return CommandHandler("start", cmd_start)


def register_extra(app):
    app.add_handler(CallbackQueryHandler(cb_check_sub, pattern="^check_sub$"))
