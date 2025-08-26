#!/bin/sh
set -e  # exit on error

# Run migrations
python manage.py migrate --noinput

# Echo the port Railway assigned
echo "PORT is: ${PORT:-<not set>}"

# Start gunicorn on the correct port
exec gunicorn DocumentManagementSystem.wsgi:application --bind 0.0.0.0:${PORT}
