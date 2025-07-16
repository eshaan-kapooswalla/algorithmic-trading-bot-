import os
from binance.client import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')

# Use the Binance Testnet endpoint
BINANCE_TESTNET_URL = 'https://testnet.binance.vision/api'

class BinanceDataClient:
    def __init__(self, api_key=API_KEY, api_secret=API_SECRET):
        self.client = Client(api_key, api_secret)
        self.client.API_URL = BINANCE_TESTNET_URL

    def get_account_info(self):
        """Fetch account information from Binance Testnet."""
        return self.client.get_account()

    def get_historical_klines(self, symbol, interval, start_str, end_str=None):
        """Fetch historical candlestick (kline) data."""
        return self.client.get_historical_klines(symbol, interval, start_str, end_str)

if __name__ == "__main__":
    bclient = BinanceDataClient()
    info = bclient.get_account_info()
    print("Account Info:", info) 