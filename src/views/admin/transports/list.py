import aiohttp_jinja2

from models import transports_tbl
from forms.transport import TransportForm


@aiohttp_jinja2.template('admin/transports.html')
async def transports_list(request):
    engine = request.app['engine']
    form = TransportForm(data={'page': request.get('page')})
    if form.validate():
        page = form.data['page']
    else:
        page = 0
    items = []
    async with engine.acquire() as conn:
        query = transports_tbl.select().offset(page * 20).limit(20)
        async for row in conn.execute(query):
            items.append({
                'id': row.id,
                'route_id': row.data['route_id'],
                'driver_id': row.data['driver_id'],
                'position': row['position']
            })
    return {
        'drivers': items
    }
