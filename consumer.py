import json
import threading
import logging

from confluent_kafka import Consumer

from flask_jwt_extended import decode_token

from app import db
from app.models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('KAFKA')


class ConsumerThread(threading.Thread):
    def __init__(self, topic, app):
        threading.Thread.__init__(self)

        self.app = app
        self.consumer = Consumer({
            # 'bootstrap.servers': 'kafka:9092',
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'login_group',
            'auto.offset.reset': 'earliest',
        })
        self.consumer.subscribe([topic])
        logger.info(f'Subscribed to topic: {topic}')
        self._running = True

    def run(self):
        logger.info("Starting consumer thread...")
        while self._running:
            msg = self.consumer.poll(timeout=5.0)

            if msg is None:
                continue
            if msg.error() is not None:
                logger.error(f'Consumer error: {msg.error().str()}')
                continue

            try:
                data_info = json.loads(msg.value().decode('utf-8'))
                event = data_info.get('event')
                access_token = data_info.get('access_token')

                if not access_token:
                    logger.error(f'Access token is missing')
                    continue

                with self.app.app_context():
                    decoded_token = decode_token(access_token)
                    logger.info(decoded_token)

                    user_id = decoded_token.get('sub').get('user_id')
                    username = decoded_token.get('sub').get('username')
                    logger.info(f'New user registered: user_id: {user_id} | username: {username}')

                    if event == 'register':
                        self.add_user(user_id, username)
            except Exception as e:
                logger.error(f"Error processing message: {e}")

        logger.info("Stopping consumer thread...")
        self.consumer.close()

    @staticmethod
    def add_user(user_id, username):
        existed_user = User.query.filter_by(username=username).first()

        if existed_user:
            logger.error(f'User {username} already exists')
            return

        new_user = User(user_id=user_id, username=username)
        db.session.add(new_user)
        db.session.commit()
        logger.info(f'User {username} added to database')

    def stop(self):
        self._running = False
        logger.info("Stopping consumer thread...")