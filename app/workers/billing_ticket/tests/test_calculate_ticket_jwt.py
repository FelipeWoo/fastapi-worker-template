

"""Integration-style tests verifying authentication is required for the endpoint.

This test ensures calls without credentials are rejected (401/403).
"""

from app.core.logger import logger


def test_calculate_requires_auth(client):
    r = client.post("/internal/billing/calculate", json={"price_usd": 10, "tax_rate": 0.16})
    logger.info("unauthenticated request status=%s body=%s", r.status_code, r.text)
    assert r.status_code in (401, 403)
