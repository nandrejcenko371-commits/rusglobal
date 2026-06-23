from telegram.ext import Application
from handlers.start import build_start_handler, register_extra
from handlers.admin import build_admin_handlers


def register_handlers(app: Application):
    app.add_handler(build_start_handler())
    for h in build_admin_handlers():
        app.add_handler(h)
    register_extra(app)
