"""Additional unit tests for `calculate_ticket` covering variants.

These verify multiple parameter combinations and expected numeric outputs.
"""

from app.workers.billing_ticket.services import calculate_ticket

from app.core.logger import logger


def test_calculate_with_fees_and_discount():
    result = calculate_ticket(200, 0.10, discount_usd=15, fees_usd=5)
    # tax = 200 * 0.10 = 20.0
    # total = 200 + 20 + 5 - 15 = 210.0
    logger.info("calculate_ticket variant: base=200, tax=0.10, discount=15, fees=5 -> %s", result)
    assert result["tax_usd"] == 20.0
    assert result["fees_usd"] == 5
    assert result["discount_usd"] == 15
    assert result["total_usd"] == 210.0


def test_calculate_zero_discount_and_fees():
    result = calculate_ticket(50, 0.2)
    # tax = 10.0, total = 60.0
    logger.info("calculate_ticket defaults: base=50, tax=0.2 -> %s", result)
    assert result["discount_usd"] == 0.0
    assert result["fees_usd"] == 0.0
    assert result["tax_usd"] == 10.0
    assert result["total_usd"] == 60.0
