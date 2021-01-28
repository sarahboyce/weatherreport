#!/bin/sh

if [ "$CHECK_POSTGRES" = "1" ]
then
    echo "Waiting for DB..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "DB started"
fi

if [ "$CHECK_REDIS" = "1" ]
then
    echo "Waiting for Redis..."

    while ! nc -z $REDIS_HOST $REDIS_PORT; do
      sleep 0.1
    done

    echo "Redis started"
fi

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --settings=weatherreport.settings.docker

# Start server
echo "Starting server"
# https://pythonspeed.com/articles/gunicorn-in-docker/
gunicorn -w 3 --max-requests 100 --log-level info --worker-tmp-dir /dev/shm --bind 0.0.0.0:8000 weatherreport.wsgi
