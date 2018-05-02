import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiopg.sa import create_engine
import asyncio

import config
import routes


def make_app():
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(config.TEMPLATE_DIR)
    )
    # setup engine
    app['engine'] = loop.run_until_complete(
        create_engine(
            user=config.DATABASE_USER, password=config.DATABASE_PASSWORD,
            host=config.DATABASE_HOST, port=config.DATABASE_PORT,
            database=config.DATABASE_NAME, loop=loop
        )
    )
    # setup urls
    routes.setup_routes(app)
    return app
