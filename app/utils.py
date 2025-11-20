"""
Utility functions for the Sports Store Order Service.

This module provides helper functions to simulate random failures and
artificial latency.  These are useful for generating alert conditions in
Prometheus/Grafana during demonstrations.
"""
import random
import time
from typing import Optional

from .config import Config


def maybe_fail() -> None:
    """Randomly raise a simulated failure.

    Based on the configured failure rate (between 0 and 1), this
    function raises a :class:`RuntimeError`.  Use this to simulate
    sporadic errors in order creation.
    """

    if random.random() < Config.FAILURE_RATE:
        raise RuntimeError("Simulated random failure in order creation")


def simulate_latency(seconds: Optional[float] = None) -> float:
    """Sleep for a number of seconds to simulate latency.

    Parameters
    ----------
    seconds: float, optional
        Number of seconds to sleep.  If not provided, the
        configured ``SIMULATED_LATENCY_SECONDS`` is used.

    Returns
    -------
    float
        The delay that was introduced.
    """

    delay = seconds if seconds is not None else Config.SIMULATED_LATENCY_SECONDS
    time.sleep(delay)
    return delay
