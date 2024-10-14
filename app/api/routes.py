from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from werkzeug.exceptions import BadRequest

from app import db
from app.models import Trailer, Truck, Vehicle
from app.api import bp


@bp.route('/transport/<transport_type>/add', methods=['POST'])
def add(transport_type):
    transport_type = transport_type.capitalize()
    form_data = request.get_json()

    try:
        main_vehicle_number = form_data.get('main_vehicle')
        additional_vehicle_number = form_data.get('connected_vehicle')

        # Get object of main vehicle number
        main_object_class = Vehicle.get_transport_type(transport_type)
        vehicle_record = main_object_class.query.filter_by(vehicle_number=main_vehicle_number).first()

        # Get object of additional vehicle number
        additional_object_class = Vehicle.get_transport_type(additional_vehicle_number)
        additional_vehicle_record = None
        if additional_object_class:
            additional_vehicle_record = additional_object_class.query.filter_by(
                vehicle_number=additional_vehicle_number).first()
    except BadRequest as e:
        return jsonify({'error': str(e), 'message': 'Bad request information'}), 400

    if vehicle_record:
        return jsonify({'success': False, 'message': f'{transport_type} {main_vehicle_number} already exists'}), 409

    vehicle_record = main_object_class(vehicle_number=main_vehicle_number)
    db.session.add(vehicle_record)
    db.session.flush()

    # Add record to relationship, if main object trailer - connect truck
    if main_object_class is Truck:
        if additional_vehicle_record:
            additional_vehicle_record.truck = vehicle_record
    elif main_object_class is Trailer:
        if additional_vehicle_record:
            additional_vehicle_record.trailer = vehicle_record
    else:
        return jsonify({'success': False, 'error': 'Invalid types'}), 400

    db.session.commit()
    return jsonify({'success': True, 'message': f'Successfully added {transport_type} {main_vehicle_number}'}), 201


@bp.route('/transport/get_trucks', methods=['GET'])
@jwt_required
def get_trucks():
    current_user = get_jwt_identity()

    trucks = Truck.query.filter_by(user_id=current_user.get('user_id'), username=current_user.get('username')).all()
