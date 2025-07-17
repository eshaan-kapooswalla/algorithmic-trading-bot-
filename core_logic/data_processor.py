"""
This module is responsible for processing the raw data fetched from the exchange.

Its primary function is to convert the raw data structures (like lists of lists)
into a more usable, powerful, and analysis-ready format, primarily the
Pandas DataFrame. This forms the foundation for all subsequent technical analysis,
feature engineering, and strategy development.
"""
import pandas as pd  # type: ignore

# It's a best practice to define the column structure from the API documentation.
# https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data
KLINE_COLUMN_NAMES = [
    'Timestamp', 
    'Open', 
    'High', 
    'Low', 
    'Close', 
    'Volume', 
    'Close_time', 
    'Quote_asset_volume', 
    'Number_of_trades', 
    'Taker_buy_base_asset_volume', 
    'Taker_buy_quote_asset_volume', 
    'Ignore'
]

# Define the essential columns we want to keep for our analysis.
ESSENTIAL_COLUMNS = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']

def create_dataframe_from_klines(klines: list) -> pd.DataFrame:
    """
    Converts a list of k-line data into a clean, indexed, and typed DataFrame.

    The function performs the following steps:
    1. Converts the raw list of lists into a DataFrame with all original columns.
    2. Selects only the essential OHLCV + Timestamp columns.
    3. Converts numeric columns ('Open', 'High', 'Low', 'Close', 'Volume')
       from string objects to high-precision numeric types.
    4. Converts the 'Timestamp' column from milliseconds-since-epoch into a
       proper datetime object.
    5. Sets the 'Timestamp' column as the DataFrame's index.
    
    Args:
        klines (list): The raw k-line data from `client.get_historical_data`.

    Returns:
        pd.DataFrame: A clean, indexed, and properly typed DataFrame.
                      Returns an empty DataFrame if the input is empty.
    """
    if not klines:
        print("Warning: klines data is empty. Returning an empty DataFrame.")
        return pd.DataFrame()

    # Create the DataFrame using the raw data and our defined column names.
    df = pd.DataFrame(klines, columns=KLINE_COLUMN_NAMES)
    
    # Select only the essential columns.
    df = df[ESSENTIAL_COLUMNS]
    
    # --- NEW: Data Type Conversion ---

    # 1. Convert price and volume columns to numeric types.
    # We use a loop for cleaner code. `pd.to_numeric` converts string to number.
    # `errors='coerce'` will turn any values that can't be converted into NaN (Not a Number).
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 2. Convert the timestamp from milliseconds (as provided by Binance) to a datetime object.
    # The `unit='ms'` is crucial for correct conversion from the Unix epoch time.
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')

    # 3. Set the 'Timestamp' column as the index of the DataFrame.
    # An index is a special column that allows for fast lookups and is essential for time-series analysis.
    df = df.set_index('Timestamp')
    
    print(f"Successfully processed {len(df)} k-lines. DataFrame is now indexed by Timestamp.")
    return df

# A self-test block to verify the functionality of this module.
if __name__ == '__main__':
    # We need to import our client functions to get some test data
    from core_logic.client import get_binance_client, get_historical_data, test_connection
    from binance.client import Client  # type: ignore
    from binance.exceptions import BinanceAPIException  # type: ignore

    try:
        # 1. Get some real data to process
        client = get_binance_client()
        klines_data = get_historical_data(
            client=client,
            symbol='BTCUSDT',
            interval=Client.KLINE_INTERVAL_1HOUR,
            start_str="2 days ago UTC"
        )

        # 2. Pass the raw data to our function
        if klines_data:
            df = create_dataframe_from_klines(klines_data)

            # 3. Inspect the result
            print("\n--- Processed DataFrame Head ---")
            print(df.head())

            print("\n--- Processed DataFrame Info ---")
            # .info() will now show a DatetimeIndex and numeric Dtypes, confirming our success!
            df.info()

    except (ValueError, BinanceAPIException, Exception) as e:
        print(f"An error occurred during the test run: {e}") 