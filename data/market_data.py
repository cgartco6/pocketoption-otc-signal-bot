import yfinance as yf
import pandas as pd

def get_1min_data(pair: str, bars: int = 100) -> pd.DataFrame:
    """
    Fetch latest 1‑minute OHLC data for a forex pair.
    """
    ticker = yf.Ticker(pair)
    # Fetch 2 hours of data to ensure enough bars
    df = ticker.history(period='2h', interval='1m')
    if df.empty:
        raise ValueError(f"No data returned for {pair}")
    return df.tail(bars)
