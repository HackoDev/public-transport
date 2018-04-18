import aiohttp_jinja2
from aiohttp.web_exceptions import HTTPFound
from sqlalchemy import delete

from models import transports_tbl


@aiohttp_jinja2.template('admin/transports-delete.html')
async def transports_delete(request):
    engine = request.app['engine']
    transport_id = request.match_info['pk']
    data = None
    async with engine.acquire() as conn:
        query = transports_tbl.select()\
            .where(transports_tbl.c.id == transport_id).limit(1)
        async for row in conn.execute(query):
            data = {
                'id': row.id,
                'route_id': row.data['route_id'],
                'driver_id': row.data['driver_id'],
            }
    if data is None:
        return {
            'instance': None
        }

    if request.method == 'POST':
        async with engine.acquire() as conn:
            await conn.execute(
                delete(transports_tbl).where(
                    transports_tbl.c.id == transport_id
                )
            )
        return HTTPFound(request.app.router['admin-transports'].url())
    return {
        'instance': data
    }
