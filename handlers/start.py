import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

import database as db
from config import CHANNEL_ID, TRAINER_URL
from messages import WELCOME, NOT_SUBSCRIBED, WELCOME_SUBSCRIBED, MAIN_MENU

logger = logging.getLogger(__name__)

MAIN_MENU_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("📚 Free Trainer", callback_data="trainer")],
    [InlineKeyboardButton("🎓 Register for Free Lesson", callback_data="kev_start")],
    [InlineKeyboardButton("💳 Join the Marathon", callback_data="payment_start")],
])


async def _check_subscription(bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status not in ("left", "kicked", "banned")
    except Exception:
        return False


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await db.add_user(user.id, user.username or "", user.first_name or "", user.last_name or "")

    subscribed = await _check_subscription(context.bot, user.id)
    if not subscribed:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Subscribe", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}")],
            [InlineKeyboardButton("✅ I'm subscribed", callback_data="check_sub")],
        ])
        await update.message.reply_text(WELCOME, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await update.message.reply_text(WELCOME_SUBSCRIBED, parse_mode="Markdown")
        await update.message.reply_text(MAIN_MENU, reply_markup=MAIN_MENU_KEYBOARD)


async def cb_check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    subscribed = await _check_subscription(context.bot, user.id)
    if not subscribed:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Subscribe", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}")],
            [InlineKeyboardButton("✅ I'm subscribed", callback_data="check_sub")],
        ])
        await query.edit_message_text(NOT_SUBSCRIBED, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await query.edit_message_text(WELCOME_SUBSCRIBED, parse_mode="Markdown")
        await query.message.reply_text(MAIN_MENU, reply_markup=MAIN_MENU_KEYBOARD)


async def cb_trainer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        f"📚 *Medical Russian Trainer*\n\nTap and start practising:\n👉 {TRAINER_URL}",
        parse_mode="Markdown",
    )


def build_start_handler() -> CommandHandler:
    return CommandHandler("start", cmd_start)


def get_extra_handlers():
    return [
        CallbackQueryHandler(cb_check_sub, pattern="^check_sub$"),
        CallbackQueryHandler(cb_trainer, pattern="^trainer$"),
    ]


# Re-export so __init__ can also register these
def register_extra(app):
    for h in get_extra_handlers():
        app.add_handler(h)
