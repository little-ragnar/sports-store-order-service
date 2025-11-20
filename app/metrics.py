"""
Prometheus metrics definitions for the Sports Store Order Service.

This module defines counters, histograms and gauges used throughout the
application.  Import the metrics you need and label them appropriately.
"""
from prometheus_client import Counter, Histogram, Gauge


# HTTP request total count labelled by method, endpoint and status
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "http_status"],
)

# HTTP request latency histogram labelled by endpoint
HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "Duration of HTTP requests in seconds",
    ["endpoint"],
)

# Total orders created labelled by status (CREATED, FAILED)
ORDERS_CREATED_TOTAL = Counter(
    "orders_created_total",
    "Total orders created",
    ["status"],
)

# Histogram of order total amount by currency
ORDERS_TOTAL_AMOUNT = Histogram(
    "orders_total_amount",
    "Distribution of order total amount",
    ["currency"],
)

# Count orders by product category
ORDERS_BY_CATEGORY = Counter(
    "orders_by_category_total",
    "Total orders by product category",
    ["category"],
)

# Internal error counter labelled by type (random failure, validation error, etc.)
ORDER_SERVICE_ERRORS_TOTAL = Counter(
    "order_service_errors_total",
    "Internal errors in order service",
    ["type"],
)

# Gauge to record simulated latency in seconds
ORDER_SERVICE_LATENCY_SIMULATED = Gauge(
    "order_service_simulated_latency_seconds",
    "Simulated latency in seconds in the /simulate-latency endpoint",
)
