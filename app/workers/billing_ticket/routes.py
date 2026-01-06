from fastapi import APIRouter, Depends

from app.core.security import require_internal_jwt
from app.workers.billing_ticket.models import TicketRequest,TicketResponse
from app.workers.billing_ticket.services import calculate_ticket

router = APIRouter(prefix="/internal/billing", tags=["billing"])


@router.post("/calculate", response_model=TicketResponse)
def calculate(
    payload: TicketRequest,
    _: dict = Depends(require_internal_jwt),
):
    return calculate_ticket(
        base_price_usd=payload.price_usd,
        tax_rate=payload.tax_rate,
        discount_usd=payload.discount_usd,
        fees_usd=payload.fees_usd,
    )
