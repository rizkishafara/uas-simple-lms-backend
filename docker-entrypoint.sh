#!/bin/sh
set -e

REDIS_HOST=${REDIS_HOST:-redis}
REDIS_PORT=${REDIS_PORT:-6379}

echo "Waiting for Redis at $REDIS_HOST:$REDIS_PORT..."
while ! nc -z "$REDIS_HOST" "$REDIS_PORT"; do
  sleep 0.5
done
echo "Redis is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating seed data..."
python manage.py seed_data

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000