from flask import current_app, jsonify, request

import sqlalchemy as sa

from app import db
from app.models import Trailer, Truck


@current_app.route('/transport/<transport_type>/add', methods=['POST'])
def add(transport_type):
    transport_type = transport_type.capitalize()
    data = request.get_json()

    if transport_type not in ['Truck', 'Trailer']:
        return jsonify({'message': 'Invalid "transport_type" parameter'}), 400
    if not data:
        return jsonify({'message': 'Empty data'}), 400

    if transport_type == 'Truck':
        truck = db.session.scalar(sa.select(Truck)).where(Truck.truck_number == data.get('truck_number'))
        if not truck:
            trailer = db.session.scalar(sa.select(Trailer)).where(Trailer.truck_number == data.get('trailer_number'))
            if not trailer:
                return jsonify({'message': f"Trailer {data.get('trailer_number')} doesn't exist"}), 400

            truck = Truck(
                truck_number=data.get('truck_number'),
                trailer=trailer
            )