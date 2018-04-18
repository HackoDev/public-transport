import aiohttp_jinja2
from aiohttp.web_exceptions import HTTPFound
from sqlalchemy import delete

from models import drivers_tbl


@aiohttp_jinja2.template('admin/drivers-delete.html')
async def drivers_delete(request):
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
            'instance': None
        }

    if request.method == 'POST':
        async with engine.acquire() as conn:
            await conn.execute(
                delete(drivers_tbl).where(drivers_tbl.c.id == driver_id)
            )
        return HTTPFound(request.app.router['admin-drivers'].url())
    return {
        'instance': data
    }
