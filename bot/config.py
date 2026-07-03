import os
from dotenv import load_dotenv
from bot.exceptions import ConfigurationError

load_dotenv()

class Config:
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
    BINANCE_BASE_URL = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")
    
    @classmethod
    def validate(cls):
        if not cls.BINANCE_API_KEY or not cls.BINANCE_SECRET_KEY:
            raise ConfigurationError("Missing Binance API credentials. Please set BINANCE_API_KEY and BINANCE_SECRET_KEY.")
