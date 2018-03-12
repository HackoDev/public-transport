import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiopg.sa import create_engine
import asyncio

import config
from models import routes_tbl


@aiohttp_jinja2.template('admin/index.html')
async def list_view(request):
    # async with engine.acquire() as conn:
    #     async for row in conn.execute(routes_tbl.select()):
    #         body += '<p>{}: {}</p>\n'.format(row.id, row.val)
    return {
        'body': 'test'
    }


def make_app():
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(config.TEMPLATE_DIR)
    )
    app['engine'] = loop.run_until_complete(
        create_engine(
            user=config.DATABASE_USER, password=config.DATABASE_PASSWORD,
            host=config.DATABASE_HOST, port=config.DATABASE_PORT,
            database=config.DATABASE_NAME, loop=loop
        )
    )
    app.router.add_get('/admin/', list_view, name='admin')
    app.router.add_static('/static/', path=config.STATIC_ROOT, name='static')
    return app
