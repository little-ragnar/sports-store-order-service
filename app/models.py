"""
In-memory data models for products and orders.

For demonstration purposes the application stores data in memory rather than
using a database.  `PRODUCTS` contains a small catalogue of sporting goods
and `ORDERS` is a dictionary keyed by order ID.
"""
from typing import Dict, List, Optional


# Predefined catalogue of sporting goods
PRODUCTS: Dict[str, Dict[str, object]] = {
    "ball-001": {
        "id": "ball-001",
        "name": "Fútbol profesional",
        "category": "football",
        "price": 35.0,
        "currency": "USD",
    },
    "shoe-010": {
        "id": "shoe-010",
        "name": "Zapatillas running",
        "category": "running",
        "price": 80.0,
        "currency": "USD",
    },
    "racket-100": {
        "id": "racket-100",
        "name": "Raqueta tenis",
        "category": "tennis",
        "price": 120.0,
        "currency": "USD",
    },
    "glove-200": {
        "id": "glove-200",
        "name": "Guante de béisbol",
        "category": "baseball",
        "price": 25.0,
        "currency": "USD",
    },
    "helmet-300": {
        "id": "helmet-300",
        "name": "Casco de ciclismo",
        "category": "cycling",
        "price": 60.0,
        "currency": "USD",
    },
}

# Orders store
ORDERS: Dict[str, Dict[str, object]] = {}
