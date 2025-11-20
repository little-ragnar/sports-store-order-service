"""
Main Flask application for the Sports Store Order Service.

This module defines the Flask application factory and all HTTP routes.
Endpoints provide a simple API for listing products, creating orders,
retrieving orders and simulating errors/latency.  Metrics are exposed
under `/metrics` for Prometheus scraping.
"""
from __future__ import annotations

import time
from typing import Any, Dict, List

from flask import Flask, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from .config import Config
from .metrics import (
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_DURATION_SECONDS,
    ORDERS_CREATED_TOTAL,
    ORDERS_TOTAL_AMOUNT,
    ORDERS_BY_CATEGORY,
    ORDER_SERVICE_ERRORS_TOTAL,
    ORDER_SERVICE_LATENCY_SIMULATED,
)
from .models import ORDERS, PRODUCTS
from .utils import maybe_fail, simulate_latency


def _record_request(method: str, endpoint: str, status_code: int, duration: float) -> None:
    """Record an HTTP request in Prometheus metrics."""

    HTTP_REQUESTS_TOTAL.labels(method, endpoint, status_code).inc()
    HTTP_REQUEST_DURATION_SECONDS.labels(endpoint).observe(duration)


def create_app() -> Flask:
    """Application factory.  Returns a configured Flask app."""

    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index() -> Any:
        start = time.time()
        data = {
            "service": Config.APP_NAME,
            "version": Config.APP_VERSION,
            "environment": Config.ENVIRONMENT,
        }
        duration = time.time() - start
        _record_request("GET", "/", 200, duration)
        return jsonify(data), 200

    @app.route("/health/live", methods=["GET"])
    def health_live() -> Any:
        start = time.time()
        duration = time.time() - start
        _record_request("GET", "/health/live", 200, duration)
        return jsonify({"status": "live"}), 200

    @app.route("/health/ready", methods=["GET"])
    def health_ready() -> Any:
        start = time.time()
        # we could perform quick dependency checks here
        duration = time.time() - start
        _record_request("GET", "/health/ready", 200, duration)
        return jsonify({"status": "ready"}), 200

    @app.route("/products", methods=["GET"])
    def list_products() -> Any:
        start = time.time()
        products = list(PRODUCTS.values())
        duration = time.time() - start
        _record_request("GET", "/products", 200, duration)
        return jsonify(products), 200

    @app.route("/products/<product_id>", methods=["GET"])
    def get_product(product_id: str) -> Any:
        start = time.time()
        product = PRODUCTS.get(product_id)
        if not product:
            duration = time.time() - start
            _record_request("GET", "/products/<product_id>", 404, duration)
            return jsonify({"error": "Product not found"}), 404
        duration = time.time() - start
        _record_request("GET", "/products/<product_id>", 200, duration)
        return jsonify(product), 200

    @app.route("/orders", methods=["POST"])
    def create_order() -> Any:
        start = time.time()
        try:
            data: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
            items: List[Dict[str, Any]] = data.get("items", [])
            if not items:
                ORDER_SERVICE_ERRORS_TOTAL.labels(type="validation_error").inc()
                duration = time.time() - start
                _record_request("POST", "/orders", 400, duration)
                return jsonify({"error": "No items provided"}), 400

            # Simulate random failure
            try:
                maybe_fail()
            except RuntimeError:
                ORDER_SERVICE_ERRORS_TOTAL.labels(type="random_failure").inc()
                ORDERS_CREATED_TOTAL.labels(status="FAILED").inc()
                duration = time.time() - start
                _record_request("POST", "/orders", 500, duration)
                return jsonify({"error": "Simulated failure"}), 500

            # Validate products and calculate totals
            total_amount: float = 0.0
            categories: set[str] = set()
            for item in items:
                product_id = item.get("product_id")
                quantity = item.get("quantity", 1)
                product = PRODUCTS.get(product_id)
                if not product:
                    ORDER_SERVICE_ERRORS_TOTAL.labels(type="validation_error").inc()
                    duration = time.time() - start
                    _record_request("POST", "/orders", 400, duration)
                    return (
                        jsonify({"error": f"Product {product_id} not found"}),
                        400,
                    )
                total_amount += float(product["price"]) * int(quantity)
                categories.add(product["category"])  # type: ignore[arg-type]

            order_id = f"ord-{len(ORDERS) + 1}"
            order_data = {
                "order_id": order_id,
                "customer_id": data.get("customer_id", "anonymous"),
                "items": items,
                "status": "CREATED",
                "total_amount": total_amount,
                "currency": "USD",
            }
            ORDERS[order_id] = order_data

            # Record business metrics
            ORDERS_CREATED_TOTAL.labels(status="CREATED").inc()
            ORDERS_TOTAL_AMOUNT.labels(currency="USD").observe(total_amount)
            for category in categories:
                ORDERS_BY_CATEGORY.labels(category=category).inc()

            duration = time.time() - start
            _record_request("POST", "/orders", 201, duration)
            return jsonify(order_data), 201

        except Exception:
            ORDER_SERVICE_ERRORS_TOTAL.labels(type="unexpected_error").inc()
            duration = time.time() - start
            _record_request("POST", "/orders", 500, duration)
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/orders/<order_id>", methods=["GET"])
    def get_order(order_id: str) -> Any:
        start = time.time()
        order = ORDERS.get(order_id)
        if not order:
            duration = time.time() - start
            _record_request("GET", "/orders/<order_id>", 404, duration)
            return jsonify({"error": "Order not found"}), 404
        duration = time.time() - start
        _record_request("GET", "/orders/<order_id>", 200, duration)
        return jsonify(order), 200

    @app.route("/orders/stats", methods=["GET"])
    def order_stats() -> Any:
        start = time.time()
        stats = {
            "total_orders": len(ORDERS),
        }
        duration = time.time() - start
        _record_request("GET", "/orders/stats", 200, duration)
        return jsonify(stats), 200

    @app.route("/simulate-error", methods=["GET"])
    def simulate_error() -> Any:
        start = time.time()
        ORDER_SERVICE_ERRORS_TOTAL.labels(type="manual_simulation").inc()
        duration = time.time() - start
        _record_request("GET", "/simulate-error", 500, duration)
        return jsonify({"error": "Simulated error endpoint"}), 500

    @app.route("/simulate-latency", methods=["GET"])
    def simulate_latency_endpoint() -> Any:
        start = time.time()
        seconds_param = request.args.get("seconds", type=float)
        delay = simulate_latency(seconds_param)
        ORDER_SERVICE_LATENCY_SIMULATED.set(delay)
        duration = time.time() - start
        _record_request("GET", "/simulate-latency", 200, duration)
        return jsonify({"delay_seconds": delay}), 200

    @app.route("/metrics")
    def metrics() -> Any:
        """Return Prometheus metrics."""
        return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

    return app


# Create a global application instance for WSGI servers (e.g. gunicorn)
application: Flask = create_app()

if __name__ == "__main__":
    # Allow running directly via python -m app.app
    application.run(host="0.0.0.0", port=8000)
