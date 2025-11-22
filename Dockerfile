## Dockerfile for Sports Store Order Service

# Use a slim Python base image with arm64 and amd64 support
FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app app

EXPOSE 8000

# Versión de la aplicación (puedes sobreescribirla con --build-arg APP_VERSION=...)
ARG APP_VERSION=0.1.0
ENV APP_VERSION=${APP_VERSION}

LABEL org.opencontainers.image.title="sports-store-order-service" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.description="Sports store order service with Prometheus metrics" \
      org.opencontainers.image.source="https://github.com/little-ragnar/sports-store-order-service"

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    APP_VERSION=${APP_VERSION}

# Use gunicorn to serve the application in production
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.app:application"]
