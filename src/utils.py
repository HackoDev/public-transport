import re

from geoalchemy2.shape import to_shape


def transform_wkt_point_to_dict(value):
    row_data = to_shape(value).to_wkt()
    m = re.match('^POINT \((?P<data>.*)\)$', row_data)
    result = {'lng': 0, 'lat': 0, }
    if m:
        lng, lat = m.groupdict()['data'].split(' ')
        result = {'lng': float(lng), 'lat': float(lat), }
    return result


def transform_wkt_line_to_dict(value):
    row_data = to_shape(value).to_wkt()
    m = re.match('^LINESTRING \((?P<data>.*)\)$', row_data)
    items = []
    if m:
        items = m.groupdict()['data'].split(',')
        items = [item.split() for item in items]
        items = [{'lng': float(item[0]), 'lat': float(item[1])}
                 for item in items]
    return items
