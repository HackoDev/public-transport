from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Table, MetaData
)
from geoalchemy2 import Geometry

metadata = MetaData()

drivers_tbl = Table(
    'drivers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String(32), nullable=False),
    Column('last_name', String(32), nullable=False),
    Column('middle_name', String(32), nullable=False),
    Column('experience', Integer, default=0),
    Column('is_active', Boolean, default=True, nullable=False)
)

routes_tbl = Table(
    'routes', metadata,
    Column('id', String(8), primary_key=True),
    Column('name', String(256), default='', nullable=False),
    Column('forward_direction', Geometry('LINESTRING'), nullable=True,
           default=None),
    Column('backward_direction', Geometry('LINESTRING'), nullable=True,
           default=None),
)

stations_tbl = Table(
    'stations', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(512), default='', nullable=False),
    Column('coord', Geometry('POINT'), default=None, nullable=True)
)

route_stations_tbl = Table(
    'route_stations', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('route_id', None, ForeignKey('routes.id'), nullable=False),
    Column('station_id', None, ForeignKey('stations.id'), nullable=False)
)

transports_tbl = Table(
    'transports', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('route_id', None, ForeignKey('routes.id'), nullable=False),
    Column('driver_id', None, ForeignKey('drivers.id'), nullable=True),
    Column('position', Geometry('POINT'), nullable=True, default=None)
)
