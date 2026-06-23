import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

import database as db
from messages import PAYMENT_SUCCESS
from config import ADMIN_CHAT_ID, EDVIBE_COURSE_LINK

logger = logging.getLogger(__name__)


def _is_admin(user_id: int) -> bool:
    return user_id == ADMIN_CHAT_ID


async def cmd_send_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Usage: /send_access USER_ID LOGIN PASSWORD
    Sends Edvibe credentials to the student and marks payment complete.
    """
    if not _is_admin(update.effective_user.id):
        return

    args = context.args
    if len(args) != 3:
        await update.message.reply_text(
            "Usage: `/send_access USER_ID LOGIN PASSWORD`",
            parse_mode="Markdown",
        )
        return

    user_id_str, login, password = args
    try:
        user_id = int(user_id_str)
    except ValueError:
        await update.message.reply_text("❌ USER_ID must be a number.")
        return

    payment = await db.get_user_payment(user_id)
    if payment is None:
        await update.message.reply_text(f"❌ No payment found for user `{user_id}`.", parse_mode="Markdown")
        return

    await db.confirm_payment(user_id, login, password)

    text = PAYMENT_SUCCESS.format(
        login=login,
        password=password,
        edvibe_link=EDVIBE_COURSE_LINK,
    )
    try:
        await context.bot.send_message(chat_id=user_id, text=text, parse_mode="Markdown")
        await update.message.reply_text(f"✅ Credentials sent to user `{user_id}`.", parse_mode="Markdown")
        logger.info("Access sent to user %s: login=%s", user_id, login)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Could not message the user: {e}")


async def cmd_pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /pending — shows all paid students waiting for Edvibe access.
    """
    if not _is_admin(update.effective_user.id):
        return

    async with __import__("aiosqlite").connect(__import__("config").DB_PATH) as db_conn:
        db_conn.row_factory = __import__("aiosqlite").Row
        async with db_conn.execute(
            "SELECT p.user_id, p.amount, p.paid_at, u.first_name, u.last_name "
            "FROM payments p LEFT JOIN users u ON p.user_id = u.user_id "
            "WHERE p.status = 'paid_pending'"
        ) as cur:
            rows = [dict(r) for r in await cur.fetchall()]

    if not rows:
        await update.message.reply_text("✅ No students waiting for access.")
        return

    lines = ["*Students without Edvibe access:*\n"]
    for r in rows:
        lines.append(
            f"👤 {r['first_name']} {r['last_name']} | ID: `{r['user_id']}` | {r['amount']} ₹\n"
            f"   `/send_access {r['user_id']} LOGIN PASSWORD`"
        )
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


def build_admin_handlers():
    return [
        CommandHandler("send_access", cmd_send_access),
        CommandHandler("pending", cmd_pending),
    ]
