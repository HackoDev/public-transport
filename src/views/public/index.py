import aiohttp_jinja2


@aiohttp_jinja2.template('public/index.html')
async def index_view(request):
    return {}
