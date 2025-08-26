FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps first (cache-friendly)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Install Python deps with cache
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Optional: remove previously baked static (if any)
RUN rm -rf staticfiles

# Build-time static collection (requires STATIC_ROOT set correctly)
RUN python manage.py collectstatic --noinput

# Start script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# (Optional) run as non-root
# RUN useradd -m appuser
# USER appuser

CMD ["sh", "/app/start.sh"]
