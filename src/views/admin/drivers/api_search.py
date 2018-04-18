import json

import aiohttp_jinja2
from sqlalchemy.sql import func

from models import drivers_tbl
from forms.driver import DriverSearchForm


async def drivers_search_list(request):
    engine = request.app['engine']
    form = DriverSearchForm(data={'search': request.get('search')})
    if form.validate():
        page = form.data['page']
    else:
        page = 0
    items = []
    search_pattern = '%{}%'
    async with engine.acquire() as conn:
        func.concat('first_name', 'last_name', 'middle_name')
        query = drivers_tbl.select(
            [(
                     drivers_tbl.c.fullname +
                     " " +
                     drivers_tbl.c.fullname.c.last_name
             ).label('full_name'), (
                     drivers_tbl.c.fullname +
                     " " +
                     drivers_tbl.c.fullname.c.last_name.substr
             ).label('full_name')]
        ).where(
            drivers_tbl.c.first_name.like(search_pattern.format())
        ).offset(page * 20).limit(20)
        async for row in conn.execute(query):
            items.append({
                'id': row.id,
                'first_name': row.first_name,
                'last_name': row.last_name,
                'middle_name': row.middle_name,
                'experience': row.experience,
                'is_active': row.is_active,
            })
    return json.dumps(items)
