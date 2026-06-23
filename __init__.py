from telegram.ext import Application
from handlers.start import build_start_handler, register_extra
from handlers.kev import build_kev_handler
from handlers.payment import build_payment_handler
from handlers.admin import build_admin_handlers


def register_handlers(app: Application):
    app.add_handler(build_start_handler())
    app.add_handler(build_kev_handler())
    for h in build_payment_handler():
        app.add_handler(h)
    for h in build_admin_handlers():
        app.add_handler(h)
    register_extra(app)
