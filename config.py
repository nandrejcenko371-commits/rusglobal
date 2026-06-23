import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@rusglobalacademy")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))

# Robokassa
ROBOKASSA_LOGIN = os.getenv("ROBOKASSA_LOGIN", "")
ROBOKASSA_PASSWORD1 = os.getenv("ROBOKASSA_PASSWORD1", "")
ROBOKASSA_PASSWORD2 = os.getenv("ROBOKASSA_PASSWORD2", "")
ROBOKASSA_TEST_MODE = os.getenv("ROBOKASSA_TEST_MODE", "1")
MARATHON_DESCRIPTION = "Марафон RusGlobal Academy"

# Pricing in INR (₹)
PRICE_EARLY = 3999.0       # до 14 июля включительно
PRICE_STANDARD = 5299.0    # с 15 по 19 июля

# Edvibe
EDVIBE_API_URL = os.getenv("EDVIBE_API_URL", "https://api.edvibe.com")
EDVIBE_API_KEY = os.getenv("EDVIBE_API_KEY", "")
EDVIBE_COURSE_ID = os.getenv("EDVIBE_COURSE_ID", "")

# Payment
PAYMENT_URL = os.getenv("PAYMENT_URL", "https://PLACEHOLDER")

# Links
ZOOM_LINK = os.getenv("ZOOM_LINK", "https://zoom.us/j/XXXXXXXXXX")
EDVIBE_COURSE_LINK = os.getenv("EDVIBE_COURSE_LINK", "https://edvibe.com/my-courses")
TRAINER_URL = "https://rusglobalacademy.in/dictionary"

# Webhook — Railway injects PORT; fall back to WEBHOOK_PORT, then 8080
WEBHOOK_PORT = int(os.getenv("PORT", os.getenv("WEBHOOK_PORT", "8080")))

# Database
DB_PATH = os.getenv("DB_PATH", "rusglobal.db")

# India Standard Time = UTC+5:30
IST = timezone(timedelta(hours=5, minutes=30))

# KEV: 17 июля 2026 в 19:00 IST
KEV_DT = datetime(2026, 7, 17, 19, 0, 0, tzinfo=IST)
KEV_REMINDER_30 = KEV_DT - timedelta(minutes=30)  # 18:30 IST
KEV_ZOOM_20 = KEV_DT - timedelta(minutes=20)       # 18:40 IST

# Marathon: 20 июля 2026 в 19:00 IST
MARATHON_DT = datetime(2026, 7, 20, 19, 0, 0, tzinfo=IST)
MARATHON_REMINDER_30 = MARATHON_DT - timedelta(minutes=30)  # 18:30 IST

WARMUP_DAYS = [1, 3, 5, 7]

# Cutoff: 15 июля 00:00 IST — с этого момента действует стандартная цена
PRICE_CUTOFF = datetime(2026, 7, 15, 0, 0, 0, tzinfo=IST)
PRICE_DEADLINE = datetime(2026, 7, 19, 23, 59, 59, tzinfo=IST)


def get_current_price() -> float:
    now = datetime.now(IST)
    return PRICE_EARLY if now < PRICE_CUTOFF else PRICE_STANDARD


def get_price_label() -> str:
    now = datetime.now(IST)
    if now < PRICE_CUTOFF:
        return f"🏷 *Early bird price* (until July 14): *₹{int(PRICE_EARLY):,}*"
    return f"💰 *Standard price*: *₹{int(PRICE_STANDARD):,}*"
