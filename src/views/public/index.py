import sqlalchemy as sa
import aiohttp_jinja2

import utils
from models import routes_tbl, route_stations_tbl, stations_tbl


@aiohttp_jinja2.template('public/index.html')
async def index_view(request):
    routes = {}
    async with request.app['engine'].acquire() as conn:
        query = sa.select([
            routes_tbl.c.id,
            routes_tbl.c.name,
            routes_tbl.c.forward_direction,
            routes_tbl.c.backward_direction,
        ]).select_from(routes_tbl)
        async for row in conn.execute(query):
            data = dict(row)
            data['forward_direction'] = \
                utils.transform_wkt_line_to_dict(data['forward_direction'])
            data['backward_direction'] = \
                utils.transform_wkt_line_to_dict(data['backward_direction'])
            joined_tables = sa.join(
                route_stations_tbl, stations_tbl,
                route_stations_tbl.c.station_id == stations_tbl.c.id
            )
            sub_query = sa.select([
                stations_tbl.c.coord,
                stations_tbl.c.name,
            ]).where(
                route_stations_tbl.c.route_id == data['id']
            ).select_from(joined_tables)
            stations = []
            async for sub_row in conn.execute(sub_query):
                stations.append({
                    'coord': utils.transform_wkt_point_to_dict(sub_row.coord),
                    'name': sub_row.name
                })
            data['stations'] = stations
            routes[str(data['id'])] = data
    return {'routes': routes}
