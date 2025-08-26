FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy files
COPY . .

COPY start.sh .
RUN chmod +x start.sh

# Set entrypoint
ENTRYPOINT ["./start.sh"]
