"""
Configuration for the Sports Store Order Service.

Values are loaded from environment variables with sensible defaults.  These
settings control the behaviour of the application such as simulated
failure rate and artificial latency.
"""
import os
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration class.

    Attributes
    ----------
    APP_NAME: str
        Name of the application for informational endpoints.
    APP_VERSION: str
        Version of the application.  Defaults to the value of the
        ``APP_VERSION`` environment variable or ``0.1.0``.
    ENVIRONMENT: str
        Deployment environment (e.g. ``local``, ``minikube``, ``production``).
    FAILURE_RATE: float
        Probability (between 0 and 1) that order creation will randomly
        fail.  Used by the :func:`app.utils.maybe_fail` helper.
    SIMULATED_LATENCY_SECONDS: float
        Number of seconds to sleep in the latency simulation endpoint.
    """

    APP_NAME: str = "sports-store-order-service"
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    FAILURE_RATE: float = float(os.getenv("FAILURE_RATE", "0.1"))
    SIMULATED_LATENCY_SECONDS: float = float(
        os.getenv("SIMULATED_LATENCY_SECONDS", "2.0")
    )
