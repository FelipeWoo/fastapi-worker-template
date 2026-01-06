"""Unit tests for `calculate_ticket` service.

These tests validate the numeric results of the billing calculation.
"""

from app.workers.billing_ticket.services import calculate_ticket

from app.core.logger import logger


def test_calculate_ticket():
    """Basic calculation: price 100, tax 16%, discount 10 => total 106."""
    result = calculate_ticket(100, 0.16, discount_usd=10)
    logger.info("calculate_ticket input: base=100, tax=0.16, discount=10 -> result=%s", result)
    assert result["total_usd"] == 106.0
