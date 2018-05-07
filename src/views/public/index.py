import json

from aiohttp.web_response import json_response
import sqlalchemy as sa
import aiohttp_jinja2

import utils
from models import routes_tbl


@aiohttp_jinja2.template('public/index.html')
async def index_view(request):
    routes = []
    async with request.app['engine'].acquire() as conn:
        query = sa.select([
            routes_tbl.c.id,
            routes_tbl.c.name,
            routes_tbl.c.forward_direction,
            routes_tbl.c.backward_direction,
        ]).select_from(routes_tbl)
        async for row in conn.execute(query):
            data = dict(row)
            data['forward_direction'] = json.dumps(
                utils.transform_wkt_line_to_dict(data['forward_direction'])
            )
            data['backward_direction'] = json.dumps(
                utils.transform_wkt_line_to_dict(data['backward_direction'])
            )
            routes.append(data)
    return {'routes': routes}
