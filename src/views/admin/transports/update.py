import aiohttp_jinja2
from aiohttp.web_exceptions import HTTPFound, HTTPNotFound
from sqlalchemy import update

from models import transports_tbl

from forms.transport import TransportForm


@aiohttp_jinja2.template('admin/transport-update.html')
async def transports_update(request):
    engine = request.app['engine']
    transport_id = request.match_info['pk']
    data = None
    async with engine.acquire() as conn:
        query = transports_tbl.select(). \
            where(transports_tbl.c.id == transport_id).limit(1)
        async for row in conn.execute(query):
            data = {
                'id': row.id,
                'route_id': row.data['route_id'],
                'driver_id': row.data['driver_id'],
                'position': row['position']
            }
    if data is None:
        return {
            'form': None,
            'instance': None
        }

    if request.method == 'POST':
        data = await request.post()
        form = TransportForm(data=data)
        if form.validate():
            async with engine.acquire() as conn:
                query = update(transports_tbl).where(
                    transports_tbl.c.id == transport_id).values(
                    route_id=form.data['route_id'],
                    driver_id=form.data['driver_id']
                )
                await conn.execute(query)
            return HTTPFound(request.app.router['admin-transports'].url())
    else:
        form = TransportForm(**data)
    return {
        'form': form,
        'instance': data
    }
