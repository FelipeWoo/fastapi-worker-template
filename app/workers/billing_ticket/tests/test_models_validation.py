"""Pydantic model validation tests for TicketRequest.

These tests assert that required fields and types are enforced by Pydantic.
"""

import pytest
from pydantic import ValidationError

from app.workers.billing_ticket.models import TicketRequest

from app.core.logger import logger


def test_ticket_request_missing_fields():
    """Missing required field should raise ValidationError."""
    # price_usd is required
    with pytest.raises(ValidationError):
        TicketRequest(tax_rate=0.16)


def test_ticket_request_bad_type():
    """Incorrect type for tax_rate should raise ValidationError."""
    # tax_rate must be a float
    with pytest.raises(ValidationError):
        TicketRequest(price_usd=10, tax_rate="not-a-number")
    logger.info("model validation tests raised expected ValidationError")
