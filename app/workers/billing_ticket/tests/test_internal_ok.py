"""Tests for internal billing calculate endpoint.

This module creates a short-lived internal JWT and calls the endpoint to
validate a successful calculation flow when authenticated.
"""


import time
import secrets
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

from app.core.logger import logger


def make_token():
    now = int(time.time())
    payload = {
        "iss": os.environ.get("INTERNAL_JWT_ISSUER", "go-main"),
        "aud": os.environ.get("INTERNAL_JWT_AUDIENCE", "fastapi-worker"),
        "iat": now,
        "exp": now + 60,
        "jti": secrets.token_hex(16),
        "sub": "service:go-main",
        "scope": "internal:billing",
    }

    secret = os.environ["INTERNAL_JWT_SECRET"]
    alg = os.environ.get("INTERNAL_JWT_ALG", "HS256")
    # sanitize alg value just in case
    alg = alg.strip().strip('"').strip("'")

    token = jwt.encode(payload, secret, algorithm=alg)
    logger.debug("generated test token: %s...", str(token)[:32])
    return token


def test_internal_calculate_ok(client):
    token = make_token()

    r = client.post(
        "/internal/billing/calculate",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "price_usd": 100,
            "tax_rate": 0.16,
            "discount_usd": 10,
        },
    )

    logger.info("internal calculate response: status=%s body=%s", r.status_code, r.text)
    assert r.status_code == 200

    body = r.json()
    assert body["base_price_usd"] == 100
    assert body["tax_usd"] == 16
    assert body["total_usd"] == 106
