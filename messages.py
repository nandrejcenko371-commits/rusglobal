from config import TRAINER_URL

# ── Onboarding ─────────────────────────────────────────────────────────────

WELCOME = (
    "Welcome to RusGlobal Academy, future doctor! 🩺🇷🇺\n\n"
    "To unlock your free trainer and all resources, "
    "please subscribe to our channel first 👇"
)

NOT_SUBSCRIBED = (
    "❌ You're not subscribed to our channel yet!\n\n"
    "Subscribe to @rusglobalacademy and tap *I'm subscribed* 👇"
)

WELCOME_SUBSCRIBED = (
    "✅ You're in!\n\n"
    "Welcome to RusGlobal Academy, future doctor! 🩺🇷🇺\n\n"
    "Here's your free trainer — *Medical Russian in 5 Minutes*:\n"
    f"👉 {TRAINER_URL}"
)

MAIN_MENU = "What would you like to do next? 👇"

# ── Warm-up ────────────────────────────────────────────────────────────────

WARMUP_1 = (
    "Hi, I'm Natalia 👋\n\n"
    "I've spent 20 years teaching languages — and built RusGlobal Academy "
    "for one reason: I kept meeting Indian medical students who could pass "
    "every test back home, but froze the moment a real Russian patient spoke to them.\n\n"
    "That's exactly what we solve here.\n\n"
    "Start with your free trainer today — just 5 minutes:\n"
    f"👉 {TRAINER_URL}"
)

WARMUP_3 = (
    "Let's talk about *NExT*. 📋\n\n"
    "The exam doesn't just test medicine — language fluency directly affects "
    "how you perform during clinical years.\n\n"
    "When a patient describes pain in rapid, colloquial Russian and you can't "
    "follow — that's not a medical gap. That's a language gap.\n\n"
    "We close that gap at RusGlobal Academy.\n\n"
    "Haven't registered for our free lesson yet? Now's the time 👇"
)

WARMUP_5 = (
    "Moving to a new country to study medicine is hard enough. 🌍\n\n"
    "The fear isn't grammar. It's the silence — that moment you understand "
    "nothing and don't know how to ask.\n\n"
    "Our students break through that silence. In real conversations, "
    "with real patients, in real clinical settings.\n\n"
    "*July 17 — Free Open Lesson (KEV)*\n"
    "📅 19:00 India time\n\n"
    "Register now — spots are limited 👇"
)

WARMUP_7 = (
    "On July 17, I'm running a *free open lesson*. 🎓\n\n"
    "You'll see exactly how we teach, what results our students get, "
    "and how you can prepare for clinical practice in Russia — even from India.\n\n"
    "📅 July 17 at 19:00 IST\n\n"
    "If you haven't registered yet — do it now. If you have — see you there! 🚀"
)

WARMUP_MSGS = {1: WARMUP_1, 3: WARMUP_3, 5: WARMUP_5, 7: WARMUP_7}

# ── KEV ───────────────────────────────────────────────────────────────────

KEV_ASK_NAME = "📝 Please enter your *full name* to register:"

KEV_ASK_PHONE = "📞 Now enter your *phone number* (e.g. +91 99999 99999):"

KEV_SUCCESS = (
    "✅ *You're registered for the free lesson!*\n\n"
    "📅 *July 17 at 19:00 IST*\n\n"
    "We'll send you a reminder 30 minutes before it starts, "
    "and the Zoom link 20 minutes before. See you there! 🎉"
)

KEV_ALREADY = (
    "✅ You're already registered for the free lesson!\n\n"
    "📅 *July 17 at 19:00 IST*\n\n"
    "We'll send your reminder and Zoom link before it starts."
)

KEV_REMINDER_30 = (
    "🔔 *Reminder!*\n\n"
    "The free open lesson starts in *30 minutes!*\n\n"
    "📅 Today at 19:00 IST\n\n"
    "Get comfortable, grab a notebook — it's going to be a great session! 📝"
)

KEV_ZOOM = (
    "🎓 *The lesson starts in 20 minutes!*\n\n"
    "Here's your Zoom link:\n"
    "👉 {zoom_link}\n\n"
    "Join a few minutes early to check your audio. See you soon! 🚀"
)

# ── Payment ────────────────────────────────────────────────────────────────

PAYMENT_INFO = (
    "🚀 *RusGlobal Academy Marathon*\n\n"
    "An intensive Russian language marathon designed for Indian medical students.\n\n"
    "📅 Start date: *July 20, 2026*\n"
    "{price_block}\n\n"
    "After payment you'll receive:\n"
    "✅ Access to the Edvibe learning platform\n"
    "✅ Your personal login and password\n"
    "✅ All marathon materials\n\n"
    "Tap the button below to pay 👇"
)

PAYMENT_PENDING = (
    "⏳ *Waiting for payment confirmation...*\n\n"
    "If you've already paid — please wait a few minutes. "
    "Your login and password will be sent here automatically."
)

PAYMENT_SUCCESS = (
    "🎉 *Payment confirmed! Welcome to the marathon!*\n\n"
    "Here are your login details for the *Edvibe* platform:\n\n"
    "👤 Login: `{login}`\n"
    "🔑 Password: `{password}`\n\n"
    "🔗 Platform: {edvibe_link}\n\n"
    "Save these details. The marathon starts *July 20 at 19:00 IST*. 🚀"
)

MARATHON_REMINDER = (
    "🔔 *The marathon starts in 30 minutes!*\n\n"
    "Log in to Edvibe now:\n"
    "🔗 {edvibe_link}\n\n"
    "👤 Login: `{login}`\n"
    "🔑 Password: `{password}`\n\n"
    "See you at the marathon! 🎉"
)
