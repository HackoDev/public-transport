import aiohttp_jinja2

from models import routes_tbl
from forms.paginator import PageForm


@aiohttp_jinja2.template('admin/routes.html')
async def list_view(request):
    engine = request.app['engine']
    form = PageForm(data={'page': request.get('page')})
    if form.validate():
        page = form.data['page']
    else:
        page = 0
    items = []
    async with engine.acquire() as conn:
        query = routes_tbl.select().offset(page * 20).limit(20)
        async for row in conn.execute(query):
            items.append({
                'id': row.id,
                'forward_direction': row.forward_direction,
                'backward_direction': row.backward_direction,
            })
    return {}
