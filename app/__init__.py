"""
Flask application factory for the Sports Store Order Service.

Importing this module and calling :func:`create_app` returns an instance
of the configured Flask application.
"""
from .app import create_app, application  # noqa: F401

__all__ = ["create_app", "application"]
