from pydantic import BaseModel


class TicketRequest(BaseModel):
    price_usd: float
    tax_rate: float
    discount_usd: float = 0.0
    fees_usd: float = 0.0


class TicketResponse(BaseModel):
    base_price_usd: float
    tax_usd: float
    discount_usd: float
    fees_usd: float
    total_usd: float
