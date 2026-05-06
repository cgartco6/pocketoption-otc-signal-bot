def moving_average(series, period: int):
    """Simple Moving Average"""
    return series.rolling(window=period).mean()
