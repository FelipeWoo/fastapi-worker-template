def calculate_ticket(
    base_price_usd: float,
    tax_rate: float,
    discount_usd: float = 0.0,
    fees_usd: float = 0.0,
) -> dict:
    tax = round(base_price_usd * tax_rate, 2)
    total = round(base_price_usd + tax + fees_usd - discount_usd, 2)

    return {
        "base_price_usd": base_price_usd,
        "tax_usd": tax,
        "discount_usd": discount_usd,
        "fees_usd": fees_usd,
        "total_usd": total,
    }
