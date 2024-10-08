import sqlalchemy as sa
import sqlalchemy.orm as so

from typing import Optional
from werkzeug.exceptions import BadRequest

from app import db


class Vehicle(db.Model):
    __abstract__ = True

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    @staticmethod
    def get_transport_type(transport_type):
        if transport_type == 'trucks':
            return Truck
        if transport_type == 'trailers':
            return Trailer
        else:
            raise BadRequest('Invalid transport type')

    @staticmethod
    def get_lists_of_vehicles():
        trucks = db.session.query(Truck).all()
        trailers = db.session.query(Trailer).all()

        truck_list = [truck.to_dict() for truck in trucks]
        trailer_list = [trailer.to_dict() for trailer in trailers]

        return truck_list, trailer_list


class Truck(Vehicle):
    __tablename__ = 'trucks'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    truck_number: so.Mapped[str] = so.mapped_column(sa.String(8), index=True, unique=True)

    trailer: so.Mapped[Optional['Trailer']] = so.relationship('Trailer', back_populates='truck', uselist=False)

    def __repr__(self):
        return f'Truck {self.truck_number}'

    def to_dict(self):
        return {
            'id': self.id,
            'truck_number': self.truck_number,
        }


class Trailer(Vehicle):
    __tablename__ = 'trailers'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    trailer_number: so.Mapped[str] = so.mapped_column(sa.String(8), index=True, unique=True)

    truck_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, sa.ForeignKey('trucks.id', ondelete='SET NULL'))
    truck: so.Mapped[Optional[Truck]] = so.relationship('Truck', back_populates='trailers', uselist=False)

    def __repr__(self):
        return f'Trailer {self.trailer_number}'

    def to_dict(self):
        return {
            'id': self.id,
            'trailer_number': self.trailer_number,
        }
