#!/usr/bin/env bash
set -e

# Fail early if critical envs are missing
if [ -z "$DB_URL" ]; then
  echo "ERROR: DB_URL is not set" >&2
  exit 1
fi

# Apply migrations at runtime (needs DATABASE_URL)
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

PORT=${PORT}
echo "Starting server on port $PORT..."

export PYTHONUNBUFFERED=1

# Start Gunicorn (update project name if different)
exec gunicorn DocumentManagementSystem.wsgi:application \
  --bind 0.0.0.0:"$PORT"
