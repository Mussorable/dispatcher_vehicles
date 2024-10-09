from flask import jsonify, request

import sqlalchemy as sa
from werkzeug.exceptions import BadRequest

from app import db
from app.models import Trailer, Truck, Vehicle
from app.api import bp


@bp.route('/transport/<transport_type>/add', methods=['POST'])
def add(transport_type):
    transport_type = transport_type.capitalize()
    form_data = request.get_json()

    vehicle = form_data.get('main_vehicle')
    connected_vehicle = form_data.get('connected_vehicle')
    dispatcher = form_data.get('dispatcher')

    try:
        transport_class = Vehicle.get_transport_type(transport_type)
        transport_object = db.session.scalar(sa.select(transport_class).where(transport_class == vehicle))
    except BadRequest as e:
        return jsonify({'error': str(e), 'message': 'Bad request information'}), 400

    if transport_class is Truck:
        pass
    elif transport_class is Trailer:
        pass
    else:
        return jsonify({'error': 'Invalid type'}), 400
