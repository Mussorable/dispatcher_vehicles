from app import create_app
from consumer import ConsumerThread

app = create_app()

consumer = ConsumerThread('user-tokens', app)
consumer.start()
