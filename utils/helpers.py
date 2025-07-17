import pandas as pd  # type: ignore
import pandas_ta as ta  # type: ignore

def format_timestamp(ts):
    """Format a timestamp as a string."""
    from datetime import datetime
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def klines_to_dataframe(klines, columns=None):
    """
    Converts raw Binance kline data (list of lists) to a pandas DataFrame with proper columns and types.
    Args:
        klines (list): Raw kline data from Binance (list of lists).
        columns (list, optional): Custom column names. If None, uses standard Binance kline columns.
    Returns:
        pd.DataFrame: DataFrame with parsed and typed columns.
    """
    if columns is None:
        columns = [
            'open_time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ]
    df = pd.DataFrame(klines, columns=columns)
    # Convert numeric columns to float
    numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume',
                    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    # Convert time columns to datetime
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    return df


def add_indicators(df, indicators=None):
    """
    Adds common technical indicators to the DataFrame using pandas-ta.
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data.
        indicators (list, optional): List of indicators to add. Defaults to ['sma', 'ema', 'rsi'].
    Returns:
        pd.DataFrame: DataFrame with new indicator columns.
    """
    if indicators is None:
        indicators = ['sma', 'ema', 'rsi']
    if 'sma' in indicators:
        df['SMA_14'] = ta.sma(df['close'], length=14)
    if 'ema' in indicators:
        df['EMA_14'] = ta.ema(df['close'], length=14)
    if 'rsi' in indicators:
        df['RSI_14'] = ta.rsi(df['close'], length=14)
    return df 