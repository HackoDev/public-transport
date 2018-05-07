from aiohttp.web_response import json_response
import sqlalchemy as sa

import utils
from models import stations_tbl


async def stations_view(request):
    stations = []
    async with request.app['engine'].acquire() as conn:
        query = sa.select([
            stations_tbl.c.name,
            stations_tbl.c.coord,
        ]).select_from(stations_tbl)
        async for row in conn.execute(query):
            data = dict(row)
            data['coord'] = utils.transform_wkt_point_to_dict(data['coord'])
            stations.append(data)
    return json_response(stations)
