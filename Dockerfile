FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static and apply migrations
RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations
RUN python manage.py migrate

# Start the app
CMD gunicorn DocumentManagementSystem.wsgi:application --bind 0.0.0.0:8080
