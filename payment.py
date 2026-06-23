from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler

import database as db
from messages import PAYMENT_INFO, PAYMENT_PENDING, PAYMENT_SUCCESS
from config import EDVIBE_COURSE_LINK, PAYMENT_URL, get_current_price, get_price_label


async def payment_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    existing = await db.get_user_payment(user_id)
    if existing and existing["status"] == "paid":
        text = PAYMENT_SUCCESS.format(
            login=existing["edvibe_login"],
            password=existing["edvibe_password"],
            edvibe_link=EDVIBE_COURSE_LINK,
        )
        await query.message.reply_text(text, parse_mode="Markdown")
        return

    price = get_current_price()
    await db.create_payment(user_id, inv_id=user_id, amount=price)

    text = PAYMENT_INFO.format(price_block=get_price_label())
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Pay now", url=PAYMENT_URL)],
        [InlineKeyboardButton("✅ I've paid — check access", callback_data="payment_check")],
    ])
    await query.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)


async def payment_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    payment = await db.get_user_payment(user_id)
    if payment and payment["status"] == "paid":
        text = PAYMENT_SUCCESS.format(
            login=payment["edvibe_login"],
            password=payment["edvibe_password"],
            edvibe_link=EDVIBE_COURSE_LINK,
        )
        await query.message.reply_text(text, parse_mode="Markdown")
    else:
        await query.message.reply_text(PAYMENT_PENDING, parse_mode="Markdown")


def build_payment_handler():
    return [
        CallbackQueryHandler(payment_entry, pattern="^payment_start$"),
        CallbackQueryHandler(payment_check, pattern="^payment_check$"),
    ]
