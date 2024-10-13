import json
import threading

import logging

from confluent_kafka import Consumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('kafka')


class ConsumerThread(threading.Thread):
    def __init__(self, topic, app):
        threading.Thread.__init__(self)

        self.app = app
        self.consumer = Consumer({
            'bootstrap.servers': 'kafka:9092',
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
                logger.info("No messages received")
                continue
            # if msg.error():
            #     logger.error(f'Consumer error: {msg.error().str()}')
            #     continue
            else:
                logger.info(f'Received message: {msg.value().decode("utf-8")}')

            try:
                logger.info(f'Message value: {msg.value()}')
                data_info = json.loads(msg.value().decode('utf-8'))
                logger.info(f'Parsed message: {data_info}')
                with self.app.app_context():
                    self.process_message(data_info)
            except Exception as e:
                logger.error(f"Error processing message: {e}")

        logger.info("Stopping consumer thread...")
        self.consumer.close()

    @staticmethod
    def process_message(data_info):
        event = data_info['event']
        access_token = data_info['access_token']

        if not access_token:
            logger.error(f'Access token is missing')
            return

        if event == 'register':
            logger.info('Register event')

    def stop(self):
        self._running = False
        logger.info("Stopping consumer thread...")