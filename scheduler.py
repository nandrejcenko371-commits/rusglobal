import logging
from datetime import datetime, timezone, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

import database as db
from config import WARMUP_DAYS
from messages import (
    WARMUP_MSGS, KEV_FORM_URL,
    BROADCAST_JULY_12, BROADCAST_JULY_15,
    BROADCAST_JULY_17_REMINDER, BROADCAST_JULY_17,
    BROADCAST_JULY_19, BROADCAST_JULY_20_PAID,
)

logger = logging.getLogger(__name__)

# All broadcast datetimes in UTC (IST = UTC+5:30)
# 12:00 IST = 06:30 UTC  |  18:40 IST = 13:10 UTC
_BROADCASTS = [
    ("july_12",          datetime(2026, 7, 12,  6, 30, tzinfo=timezone.utc), BROADCAST_JULY_12,          False),
    ("july_15",          datetime(2026, 7, 15,  6, 30, tzinfo=timezone.utc), BROADCAST_JULY_15,          False),
    ("july_17_reminder", datetime(2026, 7, 17, 13,  0, tzinfo=timezone.utc), BROADCAST_JULY_17_REMINDER, False),
    ("july_17",          datetime(2026, 7, 17, 13, 10, tzinfo=timezone.utc), BROADCAST_JULY_17,          False),
    ("july_19",          datetime(2026, 7, 19,  6, 30, tzinfo=timezone.utc), BROADCAST_JULY_19,          False),
    ("july_20",          datetime(2026, 7, 20, 13, 10, tzinfo=timezone.utc), BROADCAST_JULY_20_PAID,     True),
]


async def _send_safe(bot: Bot, chat_id: int, text: str, **kwargs):
    try:
        await bot.send_message(chat_id=chat_id, text=text, **kwargs)
    except Exception as e:
        logger.warning("Failed to send to %s: %s", chat_id, e)


async def job_warmup(bot: Bot):
    users = await db.get_all_active_users()
    now = datetime.now(timezone.utc)

    for user in users:
        sub_at = user.get("subscribed_at") or user.get("started_at")
        if not sub_at:
            continue
        subscribed = datetime.fromisoformat(sub_at)
        days_elapsed = (now.date() - subscribed.date()).days

        for day in WARMUP_DAYS:
            if days_elapsed >= day and not await db.warmup_sent(user["user_id"], day):
                text = WARMUP_MSGS[day]
                kwargs = {}
                if day == 7:
                    kwargs["reply_markup"] = InlineKeyboardMarkup([[
                        InlineKeyboardButton("Register for Free Lesson", url=KEV_FORM_URL)
                    ]])
                await _send_safe(bot, user["user_id"], text, **kwargs)
                await db.mark_warmup_sent(user["user_id"], day)
                logger.info("Warmup day %s sent to user %s", day, user["user_id"])


async def job_broadcast(bot: Bot, name: str, text: str, paid_only: bool):
    if await db.is_broadcast_sent(name):
        return

    if paid_only:
        user_ids = [p["user_id"] for p in await db.get_paid_users()]
    else:
        user_ids = [u["user_id"] for u in await db.get_all_active_users()]

    for uid in user_ids:
        await _send_safe(bot, uid, text)

    await db.mark_broadcast_sent(name)
    logger.info("Broadcast '%s' sent to %d users", name, len(user_ids))


_IST = timedelta(hours=5, minutes=30)


async def send_missed_todays_broadcasts(bot: Bot, user_id: int):
    """Send today's non-paid broadcasts that have already fired to a newly subscribed user."""
    now = datetime.now(timezone.utc)
    today_ist = (now + _IST).date()

    for name, run_date, text, paid_only in _BROADCASTS:
        if paid_only:
            continue
        if (run_date + _IST).date() != today_ist:
            continue
        if now < run_date:
            continue
        if not await db.is_broadcast_sent(name):
            continue
        await _send_safe(bot, user_id, text)


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=timezone.utc)

    # Warmup: daily at 12:00 IST = 06:30 UTC
    scheduler.add_job(job_warmup, "cron", hour=6, minute=30, args=[bot], id="warmup")

    for name, run_date, text, paid_only in _BROADCASTS:
        scheduler.add_job(
            job_broadcast, "date",
            run_date=run_date,
            args=[bot, name, text, paid_only],
            id=f"broadcast_{name}",
        )

    return scheduler
