import asyncio
import logging

from aiohttp import web
from telegram.ext import Application

from config import BOT_TOKEN, WEBHOOK_PORT
from database import init_db
from handlers import register_handlers
from scheduler import setup_scheduler
from webhook import create_web_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    await init_db()
    logger.info("Database initialized")

    app = Application.builder().token(BOT_TOKEN).build()
    register_handlers(app)

    scheduler = setup_scheduler(app.bot)
    scheduler.start()
    logger.info("Scheduler started")

    web_app = create_web_app()
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", WEBHOOK_PORT)
    await site.start()
    logger.info("Health server listening on port %d", WEBHOOK_PORT)

    async with app:
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True)
        logger.info("Bot started. Press Ctrl+C to stop.")
        await asyncio.Event().wait()  # run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped.")
