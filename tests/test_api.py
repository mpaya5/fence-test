from decimal import Decimal

import pytest


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Welcome to the Fence Test!"
    assert body["storage_backend"] == "postgres"


def test_get_interest_rate_without_data_returns_404(client, api_headers):
    response = client.get("/interest_rate", headers=api_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "No interest rate found. Please update assets first."


def test_post_asset_calculates_average_and_get_returns_it(client, api_headers):
    payload = [
        {"id": "id-1", "interest_rate": 100},
        {"id": "id-2", "interest_rate": 10},
    ]

    post_response = client.post("/asset", json=payload, headers=api_headers)
    assert post_response.status_code == 200
    assert post_response.json() == {
        "message": "Average interest rate calculated and saved successfully"
    }

    get_response = client.get("/interest_rate", headers=api_headers)
    assert get_response.status_code == 200
    body = get_response.json()
    assert Decimal(body["interest_rate"]) == Decimal("55")
    assert "updated_at" in body


def test_post_asset_overwrites_previous_rate(client, api_headers):
    client.post(
        "/asset",
        json=[{"id": "a", "interest_rate": 20}, {"id": "b", "interest_rate": 40}],
        headers=api_headers,
    )
    client.post(
        "/asset",
        json=[{"id": "c", "interest_rate": 80}],
        headers=api_headers,
    )

    response = client.get("/interest_rate", headers=api_headers)
    assert response.status_code == 200
    assert Decimal(response.json()["interest_rate"]) == Decimal("80")


@pytest.mark.parametrize(
    "headers, expected_detail",
    [
        ({}, "No API key provided"),
        ({"api_key": "wrong-key"}, "Invalid API key"),
    ],
)
def test_auth_errors(client, headers, expected_detail):
    response = client.get("/interest_rate", headers=headers)
    assert response.status_code == 403
    assert response.json()["detail"] == expected_detail


def test_post_asset_negative_rate_returns_422(client, api_headers):
    response = client.post(
        "/asset",
        json=[{"id": "id-1", "interest_rate": -5}],
        headers=api_headers,
    )
    assert response.status_code == 422


def test_post_asset_invalid_payload_returns_422(client, api_headers):
    response = client.post(
        "/asset",
        json=[{"id": "id-1"}],
        headers=api_headers,
    )
    assert response.status_code == 422
