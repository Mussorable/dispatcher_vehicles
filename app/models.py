import sqlalchemy as sa
import sqlalchemy.orm as so

from typing import Optional

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, unique=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(30), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username
        }


class Vehicle(db.Model):
    __abstract__ = True

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    @staticmethod
    def get_transport_type(transport_type):
        if transport_type == 'Truck':
            return Truck
        if transport_type == 'Trailer':
            return Trailer
        else:
            return None

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
    vehicle_number: so.Mapped[str] = so.mapped_column(sa.String(8), index=True, unique=True)

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
    vehicle_number: so.Mapped[str] = so.mapped_column(sa.String(8), index=True, unique=True)

    truck_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, sa.ForeignKey('trucks.id', ondelete='SET NULL'))
    truck: so.Mapped[Optional[Truck]] = so.relationship('Truck', back_populates='trailer', uselist=False)

    def __repr__(self):
        return f'Trailer {self.trailer_number}'

    def to_dict(self):
        return {
            'id': self.id,
            'trailer_number': self.trailer_number,
        }
