"""
FastAPI wrapper for the Binance Futures Testnet Trading Bot.
Exposes REST endpoints to place MARKET and LIMIT orders programmatically.
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import logging

from bot.client import get_testnet_client
from bot.orders import place_futures_order
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.exceptions import TradingBotException, ValidationError, ConfigurationError
from bot.logging_config import logger

app = FastAPI(
    title="Binance Futures Testnet Trading Bot API",
    description="A production-grade REST API to place MARKET and LIMIT orders on Binance USDT-M Futures Testnet.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ─── Request / Response Schemas ───────────────────────────────────────────────

class OrderRequest(BaseModel):
    symbol: str = Field(..., example="BTCUSDT", description="Trading pair symbol")
    side: str = Field(..., example="BUY", description="Order side: BUY or SELL")
    order_type: str = Field(..., alias="type", example="MARKET", description="Order type: MARKET or LIMIT")
    quantity: float = Field(..., example=0.001, description="Quantity to trade")
    price: Optional[float] = Field(None, example=105000.0, description="Price for LIMIT orders")

    model_config = {"populate_by_name": True}

    @field_validator("symbol")
    @classmethod
    def upper_symbol(cls, v):
        return v.upper()

    @field_validator("side")
    @classmethod
    def upper_side(cls, v):
        return v.upper()

    @field_validator("order_type")
    @classmethod
    def upper_type(cls, v):
        return v.upper()


class OrderResponse(BaseModel):
    order_id: str
    symbol: str
    side: str
    order_type: str
    quantity: str
    price: str
    status: str
    executed_qty: str
    avg_price: str
    timestamp: int
    result: str


# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/", summary="Health check")
def root():
    """Returns API health status."""
    return {"status": "ok", "message": "Binance Futures Testnet Trading Bot API is running."}


@app.get("/health", summary="Health check")
def health():
    """Returns API health status."""
    return {"status": "healthy"}


@app.post("/order", response_model=OrderResponse, summary="Place a Futures order")
def place_order(req: OrderRequest):
    """
    Place a MARKET or LIMIT order on Binance USDT-M Futures Testnet.

    - **symbol**: Trading pair e.g. BTCUSDT
    - **side**: BUY or SELL
    - **type**: MARKET or LIMIT
    - **quantity**: Quantity to trade
    - **price**: Required for LIMIT orders; auto-adjusted if unrealistic
    """
    try:
        symbol = validate_symbol(req.symbol)
        side = validate_side(req.side)
        order_type = validate_order_type(req.order_type)
        quantity = validate_quantity(req.quantity)
        price = validate_price(order_type, req.price)

        client = get_testnet_client()
        response = place_futures_order(
            client=client,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        logger.info(f"API order placed: {response.get('orderId')}")

        return OrderResponse(
            order_id=str(response.get("orderId", "N/A")),
            symbol=str(response.get("symbol", symbol)),
            side=str(response.get("side", side)),
            order_type=str(response.get("type", order_type)),
            quantity=str(response.get("origQty", quantity)),
            price=str(response.get("price", price or "0")),
            status=str(response.get("status", "UNKNOWN")),
            executed_qty=str(response.get("executedQty", "0")),
            avg_price=str(response.get("avgPrice", "0")),
            timestamp=int(response.get("updateTime", 0)),
            result="SUCCESS",
        )

    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except TradingBotException as e:
        logger.error(f"Trading bot error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected API error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/order/market", response_model=OrderResponse, summary="Place a MARKET order")
def place_market_order(
    symbol: str = "BTCUSDT",
    side: str = "BUY",
    quantity: float = 0.001,
):
    """Convenience endpoint for placing a MARKET order."""
    req = OrderRequest(symbol=symbol, side=side, type="MARKET", quantity=quantity)
    return place_order(req)


@app.post("/order/limit", response_model=OrderResponse, summary="Place a LIMIT order")
def place_limit_order(
    symbol: str = "BTCUSDT",
    side: str = "SELL",
    quantity: float = 0.001,
    price: Optional[float] = None,
):
    """Convenience endpoint for placing a LIMIT order."""
    req = OrderRequest(symbol=symbol, side=side, type="LIMIT", quantity=quantity, price=price)
    return place_order(req)
