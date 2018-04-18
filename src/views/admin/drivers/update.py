import aiohttp_jinja2
from aiohttp.web_exceptions import HTTPFound, HTTPNotFound
from sqlalchemy import update

from models import drivers_tbl

from forms.driver import DriverForm


@aiohttp_jinja2.template('admin/drivers-update.html')
async def drivers_update(request):
    engine = request.app['engine']
    driver_id = request.match_info['pk']
    data = None
    async with engine.acquire() as conn:
        query = drivers_tbl.select().where(drivers_tbl.c.id == driver_id) \
            .limit(1)
        async for row in conn.execute(query):
            data = {
                'id': row.id,
                'first_name': row.first_name,
                'last_name': row.last_name,
                'middle_name': row.middle_name,
                'experience': row.experience,
                'is_active': row.is_active
            }
    if data is None:
        return {
            'form': None,
            'instance': None
        }

    if request.method == 'POST':
        data = await request.post()
        form = DriverForm(data=data)
        if form.validate():
            async with engine.acquire() as conn:
                query = update(drivers_tbl).where(
                    drivers_tbl.c.id == driver_id).values(
                    first_name=form.data['first_name'],
                    last_name=form.data['last_name'],
                    middle_name=form.data['middle_name'],
                    experience=form.data['experience'],
                    is_active=form.data['is_active']
                )
                await conn.execute(query)
            return HTTPFound(request.app.router['admin-drivers'].url())
    else:
        form = DriverForm(**data)
    return {
        'form': form,
        'instance': data
    }
