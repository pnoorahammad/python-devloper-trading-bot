import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from datetime import datetime
import sys

from bot.client import get_testnet_client
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.orders import place_futures_order
from bot.logging_config import logger
from bot.exceptions import TradingBotException, ValidationError, ConfigurationError

app = typer.Typer(help="Production Binance Futures Testnet Trading Bot")
console = Console()

@app.command()
def trade(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair symbol (e.g., BTCUSDT)"),
    side: str = typer.Option(..., "--side", help="Order side: BUY or SELL"),
    order_type: str = typer.Option(..., "--type", "-t", help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Option(..., "--quantity", "-q", help="Quantity to trade"),
    price: float = typer.Option(None, "--price", "-p", help="Price (Required for LIMIT orders)")
):
    """
    Place a Market or Limit order on Binance Futures Testnet.
    """
    try:
        # Display the Trading Request details exactly as asked
        req_table = Table(title="Trading Request", show_header=False, title_style="bold blue")
        req_table.add_column("Field", style="cyan", justify="right")
        req_table.add_column("Value", style="yellow", justify="left")
        
        req_table.add_row("Symbol", symbol.upper())
        req_table.add_row("Side", side.upper())
        req_table.add_row("Order Type", order_type.upper())
        req_table.add_row("Quantity", str(quantity))
        if order_type.upper() == "LIMIT":
            req_table.add_row("Price (if limit)", str(price))
            
        console.print(Panel(req_table, border_style="blue", expand=False))

        # Validation Phase
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Validating inputs...", total=None)
            symbol = validate_symbol(symbol)
            side = validate_side(side)
            order_type = validate_order_type(order_type)
            quantity = validate_quantity(quantity)
            price = validate_price(order_type, price)

        # Execution Phase
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Authenticating with Binance API...", total=None)
            client = get_testnet_client()
            
            progress.add_task(description="Sending order request...", total=None)
            response = place_futures_order(
                client=client,
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price
            )

        # Output formatting Phase for Response
        resp_table = Table(title="Response", show_header=False, title_style="bold green")
        resp_table.add_column("Field", style="cyan", justify="right")
        resp_table.add_column("Value", style="magenta", justify="left")

        # Handle API response fields gracefully if missing
        resp_table.add_row("Order ID", str(response.get("orderId", "N/A")))
        resp_table.add_row("Status", str(response.get("status", "N/A")))
        resp_table.add_row("Executed Qty", str(response.get("executedQty", "0")))
        resp_table.add_row("Average Price", str(response.get("avgPrice", "0")))
        
        # Convert timestamp to human-readable
        update_time = response.get("updateTime")
        if update_time:
            dt = datetime.fromtimestamp(update_time / 1000)
            ts_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            ts_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
        resp_table.add_row("Timestamp", ts_str)
        
        # Determine Success or Failure visually
        status = response.get("status")
        success_msg = "[bold green]Success[/bold green]" if status in ["NEW", "FILLED", "PARTIALLY_FILLED"] else "[bold red]Failed[/bold red]"
        resp_table.add_row("Result", success_msg)

        console.print(Panel(resp_table, border_style="green", expand=False))

    except ValidationError as ve:
        logger.error(f"Validation failure: {ve}")
        console.print(f"[bold red]Validation Error:[/bold red] {ve}")
        sys.exit(1)
    except ConfigurationError as ce:
        console.print(f"[bold red]Configuration Error:[/bold red] {ce}")
        sys.exit(1)
    except TradingBotException as tbe:
        console.print(f"[bold red]Trading Bot Error:[/bold red] {tbe}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"CLI unexpected exception: {e}", exc_info=True)
        console.print(f"[bold red]An unexpected exception occurred:[/bold red] {e}")
        console.print("Check logs/trading.log for detailed stack traces.")
        sys.exit(1)

if __name__ == "__main__":
    app()
