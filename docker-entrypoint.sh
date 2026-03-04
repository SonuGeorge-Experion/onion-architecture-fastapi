#!/bin/sh
set -e

echo "Container starting..."

# echo "Waiting for database..."

# until nc -z $DB_HOST $DB_PORT; do
#   sleep 1
# done

echo "Running migrations..."
alembic upgrade head

# # Start FastAPI with Gunicorn and Uvicorn workers
# exec gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Start FastAPI app with Uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000


