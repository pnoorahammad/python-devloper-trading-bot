from bot.exceptions import ValidationError

def validate_symbol(symbol: str) -> str:
    """Validates that the symbol is a non-empty string and formats it to uppercase."""
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol must be a valid non-empty string.")
    return symbol.upper()

def validate_side(side: str) -> str:
    """Validates the order side (BUY or SELL)."""
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise ValidationError(f"Invalid side: '{side}'. Must be 'BUY' or 'SELL'.")
    return side

def validate_order_type(order_type: str) -> str:
    """Validates the order type (MARKET or LIMIT)."""
    order_type = order_type.upper()
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValidationError(f"Invalid order type: '{order_type}'. Must be 'MARKET' or 'LIMIT'.")
    return order_type

def validate_quantity(quantity: float) -> float:
    """Validates that the quantity is a positive number."""
    if quantity <= 0:
        raise ValidationError(f"Quantity must be greater than 0. Got: {quantity}")
    return quantity

def validate_price(order_type: str, price: float = None) -> float:
    """Validates that a price is provided for LIMIT orders and is a positive number."""
    if order_type == "LIMIT":
        if price is None or price <= 0:
            raise ValidationError("A positive price must be specified for LIMIT orders.")
        return price
    return price

