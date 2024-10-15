from app.models import User
from app.user_api import bp
from app import db

from flask import jsonify, request
from flask_jwt_extended import create_access_token


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return db.get_or_404(User, id).to_dict()


@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify({'users': user_list}), 200


# test_case
@bp.route('/users/<username>/add', methods=['POST'])
def add_user(username):
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Missing user_id'}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'success': False, 'message': 'User already exists'}), 409

    user = User(username=username, user_id=user_id)
    db.session.add(user)
    db.session.flush()

    access_token = create_access_token(identity={'user_id': user.user_id, 'username': user.username})

    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'User {username} created',
        'access_token': access_token
    }), 201


# test_case
@bp.route('/users/<username>/get_access_token', methods=['GET'])
def get_access_token(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User does not exist'}), 404

    access_token = create_access_token(identity={'user_id': user.user_id, 'username': user.username})
    return jsonify({'success': True, 'access_token': access_token}), 200
