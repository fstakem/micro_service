sudo service rabbitmq-server start
celery -A midmod.midmod.celery worker --loglevel=info