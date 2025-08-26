#!/usr/bin/env bash
set -e

# Railway provides $PORT
: "${PORT:=8000}"
echo "Using port: $PORT"

# Fail early if critical envs are missing
if [ -z "$SECRET_KEY" ]; then
  echo "ERROR: SECRET_KEY is not set" >&2
  exit 1
fi

# Apply migrations at runtime (needs DATABASE_URL)
python manage.py migrate --noinput

# Start Gunicorn (update project name if different)
exec gunicorn DocumentManagementSystem.wsgi:application \
  --bind 0.0.0.0:"$PORT" \
  --workers 3
