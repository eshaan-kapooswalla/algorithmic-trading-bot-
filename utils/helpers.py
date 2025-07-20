import pandas as pd  # type: ignore
import pandas_ta as ta  # type: ignore
from typing import List, Optional, Any, Dict, Union
import logging

def format_timestamp(ts: Union[int, float], fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Format a timestamp as a string.
    Args:
        ts (int | float): Timestamp (seconds since epoch).
        fmt (str): Format string for datetime.strftime.
    Returns:
        str: Formatted timestamp.
    """
    from datetime import datetime
    return datetime.fromtimestamp(ts).strftime(fmt)


def klines_to_dataframe(
    klines: List[List[Any]],
    columns: Optional[List[str]] = None,
    logger: Optional[logging.Logger] = None
) -> pd.DataFrame:
    """
    Converts raw Binance kline data (list of lists) to a pandas DataFrame with proper columns and types.
    Args:
        klines (list): Raw kline data from Binance (list of lists).
        columns (list, optional): Custom column names. If None, uses standard Binance kline columns.
        logger (logging.Logger, optional): Logger for debug output.
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
    if df.empty:
        if logger:
            logger.warning("klines_to_dataframe: Received empty klines list.")
        return df
    # Convert numeric columns to float
    numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume',
                    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']
    for col in numeric_cols:
        if col in df:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    # Convert time columns to datetime
    if 'open_time' in df:
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    if 'close_time' in df:
        df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    return df


def add_indicators(
    df: pd.DataFrame,
    indicators: Optional[List[str]] = None,
    indicator_params: Optional[Dict[str, Dict[str, Any]]] = None,
    logger: Optional[logging.Logger] = None
) -> pd.DataFrame:
    """
    Adds common technical indicators to the DataFrame using pandas-ta.
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data.
        indicators (list, optional): List of indicators to add. Defaults to ['sma', 'ema', 'rsi'].
        indicator_params (dict, optional): Dict of indicator-specific params, e.g. {'sma': {'length': 20}}.
        logger (logging.Logger, optional): Logger for debug output.
    Returns:
        pd.DataFrame: DataFrame with new indicator columns.
    """
    if df.empty:
        if logger:
            logger.warning("add_indicators: Received empty DataFrame.")
        return df
    if indicators is None:
        indicators = ['sma', 'ema', 'rsi']
    if indicator_params is None:
        indicator_params = {}
    if 'sma' in indicators:
        length = indicator_params.get('sma', {}).get('length', 14)
        df[f'SMA_{length}'] = ta.sma(df['close'], length=length)
        if logger:
            logger.info(f"Added SMA_{length}")
    if 'ema' in indicators:
        length = indicator_params.get('ema', {}).get('length', 14)
        df[f'EMA_{length}'] = ta.ema(df['close'], length=length)
        if logger:
            logger.info(f"Added EMA_{length}")
    if 'rsi' in indicators:
        length = indicator_params.get('rsi', {}).get('length', 14)
        df[f'RSI_{length}'] = ta.rsi(df['close'], length=length)
        if logger:
            logger.info(f"Added RSI_{length}")
    return df 