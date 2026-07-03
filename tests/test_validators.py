import pytest
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.exceptions import ValidationError

def test_validate_symbol():
    assert validate_symbol("btcusdt") == "BTCUSDT"
    with pytest.raises(ValidationError):
        validate_symbol("")

def test_validate_side():
    assert validate_side("buy") == "BUY"
    assert validate_side("SELL") == "SELL"
    with pytest.raises(ValidationError):
        validate_side("HOLD")

def test_validate_order_type():
    assert validate_order_type("market") == "MARKET"
    assert validate_order_type("LIMIT") == "LIMIT"
    with pytest.raises(ValidationError):
        validate_order_type("STOP")

def test_validate_quantity():
    assert validate_quantity(0.1) == 0.1
    with pytest.raises(ValidationError):
        validate_quantity(-1)

def test_validate_price():
    assert validate_price("LIMIT", 50000) == 50000
    with pytest.raises(ValidationError):
        validate_price("LIMIT", -10)
    with pytest.raises(ValidationError):
        validate_price("LIMIT", None)
    # Price should be ignored for MARKET
    assert validate_price("MARKET", None) is None
