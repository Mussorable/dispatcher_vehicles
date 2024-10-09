import json
import sqlalchemy as sa

from confluent_kafka import Consumer

from flask_jwt_extended import decode_token
from flask_jwt_extended.exceptions import JWTDecodeError
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app import db
from app.models import User


def process_user_event():
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'login_group',
        'auto.offset.reset': 'earliest',
    })

    consumer.subscribe(['user-tokens'])

    while True:
        msg = consumer.poll(timeout_ms=1000)

        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        user_info = json.loads(msg.value().decode('utf-8'))

        event = user_info['event']

        if event == 'login':
            # Decode token and get the information from db
            access_token = user_info['access_token']
            if not access_token:
                return {'error': 'Access token is missing'}

            verification_result = verify_access_token(access_token)
            if 'error' in verification_result:
                return verification_result

            decoded_token = verification_result
            user_id = decoded_token['user_id']
            username = decoded_token['username']
        elif event == 'register':
            # Add new user to db if not existed yet
            user_id = user_info['user_id']
            username = user_info['username']

            create_user_record(user_id, username)


def verify_access_token(access_token):
    try:
        decoded_token = decode_token(access_token)
        return decoded_token
    except ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except (InvalidTokenError, JWTDecodeError):
        return {'error': 'Invalid token'}


def create_user_record(user_id, username):
    user = db.session.scalar(sa.select(User).where(User.user_id == user_id))

    if not user:
        user = User(user_id=user_id, username=username)
        db.session.add(user)
        db.session.commit()
