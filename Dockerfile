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

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    APP_VERSION=${APP_VERSION:-0.1.0}

# Use gunicorn to serve the application in production
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.app:application"]
