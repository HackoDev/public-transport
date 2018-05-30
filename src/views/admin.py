import json
import re

from geoalchemy2.shape import to_shape

from forms.driver import DriverForm
from forms.route_station import RouteStationForm
from forms.transport import TransportForm
from forms.route import RouteForm
from forms.station import StationForm
from models import (
    drivers_tbl, transports_tbl, routes_tbl, stations_tbl, route_stations_tbl
)
from views.base_admin_view import TableAdminView


class DriverAdmin(TableAdminView):
    table = drivers_tbl
    list_display = ('id', 'first_name', 'last_name', 'middle_name')
    form_class = DriverForm
    verbose_name = 'Водитель'
    verbose_name_plural = 'Водители'


class TransportAdmin(TableAdminView):
    table = transports_tbl
    list_display = (
        'id', 'drivers_first_name', 'drivers_last_name',
        'route_id', 'routes_name'
    )
    form_class = TransportForm
    verbose_name = 'Траноспорт'
    verbose_name_plural = 'Траноспорт'
    change_form_template = 'admin/transport-form.html'

    lookup_fields = (
        ('route_id', (routes_tbl.name, (routes_tbl.c.name,))),
        ('driver_id', (drivers_tbl.name, (drivers_tbl.c.last_name,
                                          drivers_tbl.c.first_name,
                                          drivers_tbl.c.middle_name))),
    )

    def transform_output_data(self, data):
        if data['position'].desc:
            row_data = to_shape(data['position']).to_wkt()
            m = re.match('^POINT \((?P<data>.*)\)$', row_data)
            lng, lat = m.groupdict()['data'].split(' ')
            data['position'] = json.dumps({
                'lng': float(lng),
                'lat': float(lat),
            })
        return data

    def transform_input_data(self, data):
        if data['position']:
            row_data = json.loads(data['position'])
            data['position'] = 'POINT ({lng} {lat})'.format(
                lat=row_data['lat'], lng=row_data['lng']
            )
        else:
            data['position'] = None
        return data


class RoutesAdmin(TableAdminView):
    table = routes_tbl
    list_display = ('id', 'name')
    form_class = RouteForm
    verbose_name = 'Маршрут'
    verbose_name_plural = 'Маршруты'
    change_form_template = 'admin/route-form.html'

    def transform_input_data(self, data):
        forward_direction = json.loads(data.get('forward_direction'))
        backward_direction = json.loads(data.get('backward_direction'))
        func = lambda line: 'LINESTRING({})'.format(
            ', '.join(['{} {}'.format(x, y) for (x, y) in line])
        )
        if forward_direction:
            data['forward_direction'] = func(forward_direction)
        else:
            data['forward_direction'] = None

        if backward_direction:
            data['backward_direction'] = func(backward_direction)
        else:
            data['backward_direction'] = None

        return data

    def transform_output_data(self, data):
        if data['forward_direction'] is not None:
            row_data = to_shape(data['forward_direction']).to_wkt()
            m = re.match('^LINESTRING \((?P<data>.*)\)$', row_data)
            if m:
                items = m.groupdict()['data'].split(',')
                data['forward_direction'] = list([
                    list(map(float, item.split())) for item in items
                ])
        if data['backward_direction'] is not None:
            row_data = to_shape(data['backward_direction']).to_wkt()
            m = re.match('^LINESTRING \((?P<data>.*)\)$', row_data)
            if m:
                items = m.groupdict()['data'].split(',')
                data['backward_direction'] = list([
                    list(map(float, item.split())) for item in items
                ])
        return data


class StationsAdmin(TableAdminView):
    table = stations_tbl
    list_display = ('id', 'name')
    form_class = StationForm
    change_form_template = 'admin/station-form.html'
    verbose_name = 'Остановочная станция'
    verbose_name_plural = 'Остановочные станции'

    def transform_output_data(self, data):
        row_data = to_shape(data['coord']).to_wkt()
        m = re.match('^POINT \((?P<data>.*)\)$', row_data)
        lng, lat = m.groupdict()['data'].split(' ')
        data['coord'] = json.dumps({
            'lng': float(lng),
            'lat': float(lat),
        })
        return data

    def transform_input_data(self, data):
        row_data = json.loads(data['coord'])
        data['coord'] = 'POINT ({lng} {lat})'.format(
            lat=row_data['lat'], lng=row_data['lng']
        )
        return data


class RouteStationAdmin(TableAdminView):
    table = route_stations_tbl
    list_display = ('id', 'route_id', 'station_id')
    lookup_fields = (
        ('route_id', (routes_tbl.name, (routes_tbl.c.name,))),
        ('station_id', (stations_tbl.name, (stations_tbl.c.name,))),
    )
    form_class = RouteStationForm
    verbose_name_plural = 'Остановочные станции на маршрутах'
    verbose_name = 'Остановочная станция на маршруте'
