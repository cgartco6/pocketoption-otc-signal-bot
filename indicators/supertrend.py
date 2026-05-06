import pandas as pd
import numpy as np

def supertrend(df: pd.DataFrame, period: int = 10, multiplier: float = 3.0):
    """
    Calculate Supertrend indicator.
    Returns: (supertrend, direction)
    direction = 1 for uptrend (green), -1 for downtrend (red)
    """
    hl2 = (df['High'] + df['Low']) / 2
    atr = df['High'].rolling(period).max() - df['Low'].rolling(period).min()
    upper_band = hl2 + (multiplier * atr)
    lower_band = hl2 - (multiplier * atr)
    
    supertrend = pd.Series(index=df.index, dtype=float)
    direction = pd.Series(index=df.index, dtype=int)
    
    for i in range(period, len(df)):
        if i == period:
            supertrend.iloc[i] = upper_band.iloc[i]
            direction.iloc[i] = 1
        else:
            if upper_band.iloc[i] < supertrend.iloc[i-1]:
                supertrend.iloc[i] = upper_band.iloc[i]
                direction.iloc[i] = 1
            else:
                supertrend.iloc[i] = lower_band.iloc[i]
                direction.iloc[i] = -1
    return supertrend, direction
