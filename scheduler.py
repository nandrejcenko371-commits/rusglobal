import logging
from datetime import datetime, timezone, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot

import database as db
from config import (
    KEV_REMINDER_30, KEV_ZOOM_20, MARATHON_REMINDER_30,
    ZOOM_LINK, EDVIBE_COURSE_LINK, ADMIN_CHAT_ID, WARMUP_DAYS,
)
from messages import WARMUP_MSGS, KEV_REMINDER_30 as MSG_KEV_30, KEV_ZOOM, MARATHON_REMINDER

logger = logging.getLogger(__name__)


async def _send_safe(bot: Bot, chat_id: int, text: str, **kwargs):
    try:
        await bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown", **kwargs)
    except Exception as e:
        logger.warning("Failed to send to %s: %s", chat_id, e)


# ── Warm-up ────────────────────────────────────────────────────────────────

async def job_warmup(bot: Bot):
    users = await db.get_all_active_users()
    now = datetime.now(timezone.utc)

    for user in users:
        started = datetime.fromisoformat(user["started_at"])
        days_elapsed = (now - started).days

        for day in WARMUP_DAYS:
            if days_elapsed >= day and not await db.warmup_sent(user["user_id"], day):
                text = WARMUP_MSGS[day].format(name=user["first_name"] or "друг")
                await _send_safe(bot, user["user_id"], text)
                await db.mark_warmup_sent(user["user_id"], day)
                logger.info("Warmup day %s sent to %s", day, user["user_id"])


# ── KEV reminders ─────────────────────────────────────────────────────────

async def job_kev_reminder_30(bot: Bot):
    user_ids = await db.get_kev_users_pending("reminder_sent")
    for uid in user_ids:
        await _send_safe(bot, uid, MSG_KEV_30)
        await db.mark_kev_flag(uid, "reminder_sent")
    logger.info("KEV 30-min reminder sent to %d users", len(user_ids))


async def job_kev_zoom_20(bot: Bot):
    user_ids = await db.get_kev_users_pending("zoom_sent")
    text = KEV_ZOOM.format(zoom_link=ZOOM_LINK)
    for uid in user_ids:
        await _send_safe(bot, uid, text)
        await db.mark_kev_flag(uid, "zoom_sent")
    logger.info("KEV Zoom link sent to %d users", len(user_ids))


# ── Marathon reminder ──────────────────────────────────────────────────────

async def job_marathon_reminder(bot: Bot):
    paid_users = await db.get_paid_users_pending_reminder()
    for payment in paid_users:
        text = MARATHON_REMINDER.format(
            edvibe_link=EDVIBE_COURSE_LINK,
            login=payment["edvibe_login"],
            password=payment["edvibe_password"],
        )
        await _send_safe(bot, payment["user_id"], text)
        await db.mark_marathon_reminder_sent(payment["user_id"])
    logger.info("Marathon reminder sent to %d users", len(paid_users))


# ── Setup ──────────────────────────────────────────────────────────────────

def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=timezone.utc)

    # Warm-up: check every hour (handles day-level precision)
    scheduler.add_job(job_warmup, "interval", hours=1, args=[bot], id="warmup")

    # KEV: fixed datetimes (UTC)
    scheduler.add_job(
        job_kev_reminder_30, "date",
        run_date=KEV_REMINDER_30.astimezone(timezone.utc),
        args=[bot], id="kev_30",
    )
    scheduler.add_job(
        job_kev_zoom_20, "date",
        run_date=KEV_ZOOM_20.astimezone(timezone.utc),
        args=[bot], id="kev_20",
    )

    # Marathon: fixed datetime (UTC)
    scheduler.add_job(
        job_marathon_reminder, "date",
        run_date=MARATHON_REMINDER_30.astimezone(timezone.utc),
        args=[bot], id="marathon_30",
    )

    return scheduler
