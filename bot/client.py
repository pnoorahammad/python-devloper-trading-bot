import os
from binance.client import Client
from bot.config import Config
from bot.exceptions import ConfigurationError
from bot.logging_config import logger

def get_testnet_client() -> Client:
    """
    Initializes and returns a Binance Client configured for the Futures Testnet.
    """
    try:
        Config.validate()
        
        # Initialize the client
        client = Client(Config.BINANCE_API_KEY, Config.BINANCE_SECRET_KEY, testnet=True)
        
        logger.info(f"Binance Futures Testnet Client initialized. Base URL: {Config.BINANCE_BASE_URL}")
        return client
    except ConfigurationError as e:
        logger.error(f"Configuration Error: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to initialize Binance Client: {e}", exc_info=True)
        raise
