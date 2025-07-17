"""
This module is responsible for processing the raw data fetched from the exchange.

Its primary function is to convert the raw data structures (like lists of lists)
into a more usable, powerful, and analysis-ready format, primarily the
Pandas DataFrame. This forms the foundation for all subsequent technical analysis,
feature engineering, and strategy development.
"""
import pandas as pd  # type: ignore
import pandas_ta as ta  # type: ignore

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
    
    # 1. Convert price and volume columns to numeric types.
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 2. Convert the timestamp from milliseconds (as provided by Binance) to a datetime object.
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')

    # 3. Set the 'Timestamp' column as the index of the DataFrame.
    df = df.set_index('Timestamp')
    
    print(f"Successfully processed {len(df)} k-lines. DataFrame is now indexed by Timestamp.")
    return df

# --- NEW FUNCTION ---
def add_sma(df: pd.DataFrame, period: int = 50) -> pd.DataFrame:
    """
    Calculates the Simple Moving Average (SMA) and adds it as a new column.

    Args:
        df (pd.DataFrame): The input DataFrame with at least a 'Close' column.
        period (int): The lookback period for the SMA calculation. Defaults to 50.

    Returns:
        pd.DataFrame: The DataFrame with the new 'SMA_{period}' column added.
    """
    print(f"Calculating {period}-period SMA...")
    df.ta.sma(length=period, append=True)
    print("SMA calculation complete.")
    return df

def add_ema(df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    """
    Calculates the Exponential Moving Average (EMA) and adds it as a new column.

    The EMA gives more weight to recent prices, making it more responsive than the SMA.

    Args:
        df (pd.DataFrame): The input DataFrame with at least a 'Close' column.
        period (int): The lookback period for the EMA calculation. Defaults to 20.

    Returns:
        pd.DataFrame: The DataFrame with the new 'EMA_{period}' column added.
    """
    print(f"Calculating {period}-period EMA...")
    df.ta.ema(length=period, append=True)
    print("EMA calculation complete.")
    return df

if __name__ == '__main__':
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
            start_str="5 days ago UTC"
        )

        if klines_data:
            # 2. Process the raw data into a clean DataFrame
            df = create_dataframe_from_klines(klines_data)

            # 3. Add the indicators to our DataFrame
            df = add_sma(df, period=50)
            df = add_ema(df, period=20)

            # 4. Inspect the result
            print("\n--- DataFrame with SMA and EMA ---")
            print(df.tail(10))

    except (ValueError, BinanceAPIException, Exception) as e:
        print(f"An error occurred during the test run: {e}") 