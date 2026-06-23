from aiohttp import web


async def healthcheck(request: web.Request) -> web.Response:
    return web.Response(text="ok")


def create_web_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", healthcheck)
    return app
