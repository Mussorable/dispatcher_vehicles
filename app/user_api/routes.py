from app.models import User
from app.user_api import bp
from app import db

from flask import jsonify, request


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return db.get_or_404(User, id).to_dict()


@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify({'users': user_list}), 200


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
    db.session.commit()

    return jsonify({'success': True, 'message': f'User {username} created'}), 201
