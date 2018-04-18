import aiohttp_jinja2
from aiohttp.web_exceptions import HTTPFound

from models import transports_tbl
from forms.transport import TransportForm


@aiohttp_jinja2.template('admin/transports-add.html')
async def transports_add(request):
    engine = request.app['engine']
    if request.method == 'POST':
        data = await request.post()
        form = TransportForm(data)
        if form.validate():
            position = 'POINT({lat} {lng})'.format(
                lat=form.data['latitude'],
                lng=form.data['longitude']
            )
            async with engine.acquire() as conn:
                await conn.execute(transports_tbl.insert().values(
                    position=position,
                    route_id=form.data['route_id'],
                    driver_id=form.data['driver_id']
                ))
                return HTTPFound(request.app.router['admin-transports'].url())
    else:
        form = TransportForm()
    return {
        'form': form
    }
