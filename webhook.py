"""
Aiohttp server that receives Robokassa ResultURL notifications.
After payment confirmation the admin is notified — no Edvibe API needed.
"""

import logging
from aiohttp import web
from telegram import Bot

import database as db
from robokassa import verify_result_signature
from config import ADMIN_CHAT_ID

logger = logging.getLogger(__name__)

ADMIN_NOTIFY = (
    "💰 *New marathon payment!*\n\n"
    "👤 Name: {first_name} {last_name}\n"
    "🆔 Telegram ID: `{user_id}`\n"
    "💵 Amount: {amount} ₹\n\n"
    "Register the student in Edvibe, then send their credentials:\n"
    "`/send_access {user_id} LOGIN PASSWORD`"
)

STUDENT_PAYMENT_CONFIRM = (
    "✅ *Payment received!*\n\n"
    "We're setting up your access to the Edvibe platform.\n"
    "You'll receive your login and password here within a few hours. 🎓"
)


async def robokassa_result(request: web.Request) -> web.Response:
    bot: Bot = request.app["bot"]

    try:
        data = await request.post()
        out_sum = data.get("OutSum", "")
        inv_id  = data.get("InvId", "")
        sig     = data.get("SignatureValue", "")

        if not verify_result_signature(out_sum, inv_id, sig):
            logger.warning("Bad Robokassa signature: inv_id=%s", inv_id)
            return web.Response(text="bad signature", status=400)

        inv_id_int = int(inv_id)
        payment = await db.get_payment_by_inv(inv_id_int)

        if payment is None:
            logger.warning("Unknown inv_id=%s", inv_id)
            return web.Response(text="unknown inv", status=404)

        if payment["status"] == "paid":
            return web.Response(text=f"OK{inv_id}")

        user_id = payment["user_id"]
        await db.mark_payment_paid_pending_access(inv_id_int)

        user = await db.get_user(user_id)
        first_name = user["first_name"] if user else ""
        last_name  = user["last_name"]  if user else ""

        # Notify student — access will come soon
        try:
            await bot.send_message(
                chat_id=user_id,
                text=STUDENT_PAYMENT_CONFIRM,
                parse_mode="Markdown",
            )
        except Exception as e:
            logger.warning("Could not notify student %s: %s", user_id, e)

        # Notify admin to register in Edvibe manually
        if ADMIN_CHAT_ID:
            await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=ADMIN_NOTIFY.format(
                    first_name=first_name,
                    last_name=last_name,
                    user_id=user_id,
                    amount=payment["amount"],
                ),
                parse_mode="Markdown",
            )

        logger.info("Payment confirmed: inv_id=%s user_id=%s", inv_id, user_id)
        return web.Response(text=f"OK{inv_id}")

    except Exception as e:
        logger.exception("Webhook error: %s", e)
        return web.Response(text="error", status=500)


def create_web_app(bot: Bot) -> web.Application:
    app = web.Application()
    app["bot"] = bot
    app.router.add_post("/robokassa/result", robokassa_result)
    return app
