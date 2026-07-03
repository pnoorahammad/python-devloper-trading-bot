from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.logging_config import logger
from bot.exceptions import APIError, NetworkError

def place_futures_order(
    client: Client,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None
) -> dict:
    """
    Places an order on Binance Futures Testnet (USDT-M).
    
    Args:
        client: The Binance client instance.
        symbol: Trading pair symbol (e.g., 'BTCUSDT').
        side: 'BUY' or 'SELL'.
        order_type: 'MARKET' or 'LIMIT'.
        quantity: Amount to trade.
        price: Price for LIMIT orders.
        
    Returns:
        dict: The order response from Binance.
    """
    endpoint = "/fapi/v1/order"
    try:
        logger.info(f"Preparing to place {order_type} {side} order for {quantity} of {symbol}")
        
        # Base order parameters
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }
        
        # Add required parameters for LIMIT orders
        if order_type == "LIMIT":
            params['price'] = price
            params['timeInForce'] = 'GTC' # Good Till Canceled
            
        # Log request payload details
        logger.debug(f"HTTP Request: POST {endpoint}")
        logger.debug(f"Payload: {params}")
        
        # Place the futures order
        response = client.futures_create_order(**params)
        
        logger.info(f"Order placed successfully. Order ID: {response.get('orderId')}")
        logger.debug(f"Response: {response}")
        
        return response
        
    except BinanceAPIException as e:
        logger.error(f"Binance API Exception at {endpoint}: Status Code {e.status_code}, Message: {e.message}", exc_info=True)
        raise APIError(f"API Error ({e.status_code}): {e.message}")
    except BinanceRequestException as e:
        logger.error(f"Binance Request Exception at {endpoint}: Network failure - {e}", exc_info=True)
        raise NetworkError(f"Network/Request Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while placing order at {endpoint}: {e}", exc_info=True)
        raise APIError(f"Unexpected Error: {str(e)}")
