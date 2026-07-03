class TradingBotException(Exception):
    """Base exception for the trading bot."""
    pass

class ConfigurationError(TradingBotException):
    """Raised when environment variables are missing or incorrect."""
    pass

class ValidationError(TradingBotException):
    """Raised when user input validation fails."""
    pass

class APIError(TradingBotException):
    """Raised when the Binance API returns an error."""
    pass

class NetworkError(TradingBotException):
    """Raised when a network or connection error occurs."""
    pass
