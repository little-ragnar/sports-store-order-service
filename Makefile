# Convenience commands for local development

.PHONY: help test lint run build

help:
	@echo "Available make targets:"
	@echo "  test    Run unit tests with pytest"
	@echo "  run     Run the application locally"
	@echo "  build   Build the Docker image"

test:
	pytest

run:
	python -m app.app

build:
	docker build -t sports-store-order-service:latest .
