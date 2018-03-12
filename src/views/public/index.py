import aiohttp_jinja2


@aiohttp_jinja2.template('admin/index.html')
async def list_view(request):
    # async with engine.acquire() as conn:
    #     async for row in conn.execute(routes_tbl.select()):
    #         body += '<p>{}: {}</p>\n'.format(row.id, row.val)
    return {
        'body': 'test'
    }
