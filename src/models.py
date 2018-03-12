from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

metadata = MetaData()
BaseModel = declarative_base(metadata=metadata)


class Driver(BaseModel):
    __tablename__ = 'drivers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    middle_name = Column(String(32), nullable=False)
    experience = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, nullable=False)


class Route(BaseModel):
    __tablename__ = 'routes'

    id = Column(String(8), primary_key=True)
    forward_direction = Column(Geometry('MULTILINESTRING'), nullable=True,
                               default=None)
    backward_direction = Column(Geometry('MULTILINESTRING'), nullable=True,
                                default=None)


class Station(BaseModel):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(512), default='', nullable=False)
    coord = Column(Geometry('POINT'), default=None, nullable=True)


class RouteStations(BaseModel):
    __tablename__ = 'route_stations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(ForeignKey('routes.id'), nullable=False)
    station_id = Column(ForeignKey('stations.id'), nullable=False)


class Transport(BaseModel):
    __tablename__ = 'transports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(ForeignKey('routes.id'), nullable=False)
    driver_id = Column(ForeignKey('drivers.id'), nullable=False)
    position = Column(Geometry('POINT'), nullable=True, default=None)
