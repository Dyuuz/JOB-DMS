FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy files
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static and apply migrations
# Remove old static files
RUN rm -rf staticfiles

# Collect new static files
RUN python manage.py collectstatic --noinput

# DO NOT run makemigrations here unless you know what you're doing
# RUN python manage.py makemigrations

# Run migrate and start the app at runtime
CMD ["sh", "-c", "python manage.py migrate && gunicorn DocumentManagementSystem.wsgi:application --bind 0.0.0.0:8080"]
