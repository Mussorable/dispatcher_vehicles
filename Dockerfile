FROM severstaldigital/python-librdkafka:latest

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY migrations migrations
COPY manager.py config.py consumer.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP=manager.py

EXPOSE 5001
ENTRYPOINT ["./boot.sh"]