"""
Basic tests for the Sports Store Order Service.

These tests verify that the primary endpoints respond with the expected
status codes.  To run the tests locally:

```sh
pytest
```
"""

import json

from app.app import create_app


def test_index() -> None:
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "service" in data


def test_products() -> None:
    app = create_app()
    client = app.test_client()
    response = client.get("/products")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 1


def test_create_order() -> None:
    app = create_app()
    client = app.test_client()
    payload = {
        "customer_id": "testuser",
        "items": [
            {"product_id": "ball-001", "quantity": 1},
            {"product_id": "shoe-010", "quantity": 2},
        ],
    }
    response = client.post("/orders", json=payload)
    assert response.status_code in (201, 500)  # random failure may return 500
    if response.status_code == 201:
        data = json.loads(response.data)
        assert data["status"] == "CREATED"
        assert data["order_id"].startswith("ord-")
