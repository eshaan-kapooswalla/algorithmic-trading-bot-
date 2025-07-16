"""
This module encapsulates all interactions with the Binance API.

It is responsible for:
- Initializing the API client with credentials from the environment.
- Fetching market data (e.g., historical k-lines, latest price).
- Managing account information (e.g., fetching balance).
- Executing, checking, and canceling orders.

The rest of the application should not interact with the `python-binance`
library directly. Instead, it should use the clean, high-level functions
provided by this module. This design pattern, often called a "Client,"
"Service," or "Wrapper," is crucial for creating maintainable and testable
code by decoupling our application's core logic from the specific details
of an external service (the exchange API).
"""

import os
import time
import functools
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException
from requests.exceptions import ConnectionError, Timeout

# --- NEW: Retry Decorator ---
def retry(max_retries=3, backoff_factor=2):
    """A decorator for retrying a function call with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except BinanceAPIException as e:
                    if e.status_code in [429, 418]:
                        retries += 1
                        if retries >= max_retries:
                            print("Max retries reached for rate limit. Aborting.")
                            raise e
                        delay = backoff_factor ** retries
                        print(f"Rate limit hit. Retrying in {delay} seconds... (Attempt {retries}/{max_retries})")
                        time.sleep(delay)
                    else:
                        print(f"Binance API Error (non-retriable): {e}")
                        raise e
                except (ConnectionError, Timeout) as e:
                    retries += 1
                    if retries >= max_retries:
                        print("Max retries reached for network error. Aborting.")
                        raise e
                    delay = backoff_factor ** retries
                    print(f"Network error: {e}. Retrying in {delay} seconds... (Attempt {retries}/{max_retries})")
                    time.sleep(delay)
                except Exception as e:
                    print(f"An unexpected error occurred in {func.__name__}: {e}")
                    raise e
            raise Exception(f"Failed to execute {func.__name__} after {max_retries} retries.")
        return wrapper
    return decorator

def get_binance_client() -> Client:
    """Loads API credentials from a .env file and initializes the Binance client."""
    load_dotenv()
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        raise ValueError("Binance API key and/or secret not found. ...")
    client = Client(api_key, api_secret)
    client.API_URL = 'https://testnet.binance.vision/api'
    print("Binance client initialized successfully for Testnet.")
    return client

@retry()
def test_connection(client: Client):
    """Tests the API connection by fetching account information."""
    print("Testing connection...")
    account_info = client.get_account()
    balances = account_info['balances']
    print("Connection Successful. Account balances:")
    assets_to_check = ['USDT', 'BTC', 'ETH', 'BNB']
    for asset in balances:
        if asset['asset'] in assets_to_check:
            print(f"  - {asset['asset']}: {asset['free']} (Free), {asset['locked']} (Locked)")

@retry()
def get_historical_data(client: Client, symbol: str, interval: str, start_str: str) -> list:
    """Fetches historical candlestick (k-line) data for a given symbol."""
    print(f"Fetching historical k-line data for {symbol} with interval {interval} from {start_str}...")
    klines = client.get_historical_klines(symbol, interval, start_str)
    if not klines:
        print(f"Warning: No data found for {symbol} with the specified parameters.")
        return []
    print(f"Successfully fetched {len(klines)} k-lines for {symbol}.")
    return klines

@retry()
def get_latest_price(client: Client, symbol: str) -> dict | None:
    """Fetches the latest price ticker for a specific symbol."""
    print(f"Fetching latest price for {symbol}...")
    ticker = client.get_symbol_ticker(symbol=symbol)
    print(f"Successfully fetched ticker: {ticker}")
    return ticker

if __name__ == '__main__':
    try:
        binance_client = get_binance_client()
        test_connection(binance_client)
        print("\n" + "="*50 + "\n")
        symbol_to_fetch = 'BTCUSDT'
        historical_klines = get_historical_data(
            client=binance_client,
            symbol=symbol_to_fetch,
            interval=Client.KLINE_INTERVAL_1HOUR,
            start_str="1 day ago UTC"
        )
        print("\n" + "="*50 + "\n")
        # Test with an invalid symbol to see non-retriable error handling
        try:
            print("Testing with an invalid symbol (should fail without retrying)...")
            get_latest_price(client=binance_client, symbol='NOTAREALSYMBOL')
        except BinanceAPIException as e:
            print(f"Successfully caught expected error for invalid symbol: {e.message}")
    except (ValueError, BinanceAPIException, Exception) as e:
        print(f"\nAn error occurred during the script execution: {e}") 