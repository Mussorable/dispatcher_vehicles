import logging
import sqlalchemy as sa
import sqlalchemy.orm as so

from app import create_app, db
from consumer import ConsumerThread

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('kafka')

app = create_app()

consumer = ConsumerThread('user-tokens', app)
consumer.start()

if not consumer.is_alive():
    logger.info('Consumer thread is not running')
else:
    logger.info('Consumer thread is running')


@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'sa': sa, 'so': so, 'consumer': consumer}
