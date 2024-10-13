import multiprocessing

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import create_app, db
from consumer import ConsumerThread

app = create_app()


def start_consumer():
    consumer = ConsumerThread('user-tokens', app)
    consumer.start()


consumer_process = multiprocessing.Process(target=start_consumer)
consumer_process.start()


@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'sa': sa, 'so': so}
