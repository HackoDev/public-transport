import aiohttp_jinja2

from models import drivers_tbl
from forms.paginator import PageForm


@aiohttp_jinja2.template('admin/drivers.html')
async def drivers_list(request):
    engine = request.app['engine']
    form = PageForm(data={'page': request.get('page')})
    if form.validate():
        page = form.data['page']
    else:
        page = 0
    items = []
    async with engine.acquire() as conn:
        query = drivers_tbl.select().offset(page * 20).limit(20)
        async for row in conn.execute(query):
            items.append({
                'id': row.id,
                'first_name': row.first_name,
                'last_name': row.last_name,
                'middle_name': row.middle_name,
                'experience': row.experience,
                'is_active': row.is_active,
            })
    return {
        'drivers': items
    }
