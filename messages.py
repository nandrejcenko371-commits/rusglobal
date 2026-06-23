from config import TRAINER_URL

KEV_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdIU2jif9AMvwNRLigJizpquxSYyyEQGi7pMbzaI41mxvRkvw/viewform"

# ── Onboarding ──────────────────────────────────────────────────────────────

WELCOME_NOT_SUBSCRIBED = (
    "To get your free trainer, please subscribe to our channel first "
    "👉 @rusglobalacademy\n\n"
    "Once you're subscribed, tap the button below."
)

NOT_SUBSCRIBED_AGAIN = (
    "❌ Looks like you're not subscribed yet.\n\n"
    "Subscribe to @rusglobalacademy and tap the button again 👇"
)

TRAINER_MSG = (
    "Here's your free trainer — Medical Russian in 5 Minutes:\n"
    f"👉 {TRAINER_URL}"
)

# ── Warm-up ─────────────────────────────────────────────────────────────────

WARMUP_1 = (
    "Hi, I'm Natalia 👋 I've spent 20 years teaching languages — and built RusGlobal Academy "
    "for one reason: I kept meeting Indian medical students who could pass "
    "every test back home, but froze the moment a real Russian patient spoke to them."
)

WARMUP_3 = (
    "Let's talk about NExT. The exam doesn't just test medicine — language fluency directly affects "
    "how you perform during clinical years."
)

WARMUP_5 = (
    "Moving to a new country to study medicine is hard enough. "
    "The fear isn't grammar. It's the silence."
)

WARMUP_7 = (
    f"On July 17, I'm running a free open lesson. Register here 👉 {KEV_FORM_URL}"
)

WARMUP_MSGS = {1: WARMUP_1, 3: WARMUP_3, 5: WARMUP_5, 7: WARMUP_7}

# ── Calendar broadcasts ──────────────────────────────────────────────────────

BROADCAST_JULY_12 = (
    "Just a reminder: early-bird pricing (₹3,999) ends July 14. "
    "After that — ₹5,299.\n\n"
    "Reserve your spot 👉 https://edvibe.com/marathon-register/126120"
)

BROADCAST_JULY_15 = (
    "The free open lesson is this Thursday, July 17 at 19:00 India time.\n\n"
    f"Save your spot 👉 {KEV_FORM_URL}"
)

BROADCAST_JULY_17_REMINDER = (
    "🔔 We start in 30 minutes! Get ready — see you at 19:00 India time."
)

BROADCAST_JULY_17 = (
    "🎙️ We're starting in 20 minutes!\n\n"
    "Join here 👉 https://us06web.zoom.us/j/86841139458?pwd=j5WPSSei0ayg9z2oqbu8bJbY8F4Gaa.1"
)

BROADCAST_JULY_19 = (
    "Yesterday was just a taste. The full Russian for Survival Marathon starts July 20.\n\n"
    "Join now 👉 https://edvibe.com/marathon-register/126120 — ₹5,299"
)

BROADCAST_JULY_20_PAID = (
    "The marathon starts in 20 minutes!\n\n"
    "The link is in your personal account on Edvibe 👉 https://app.edvibe.com"
)

# ── Admin / Payment ──────────────────────────────────────────────────────────

PAYMENT_SUCCESS = (
    "🎉 *Payment confirmed! Welcome to the marathon!*\n\n"
    "Here are your login details for the *Edvibe* platform:\n\n"
    "👤 Login: `{login}`\n"
    "🔑 Password: `{password}`\n\n"
    "🔗 Platform: {edvibe_link}\n\n"
    "Save these details. The marathon starts *July 20 at 19:00 IST*. 🚀"
)
