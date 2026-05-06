import pandas as pd
import numpy as np

def zigzag(high: pd.Series, low: pd.Series, depth: int = 12, deviation: int = 5, backstep: int = 3) -> pd.Series:
    """
    Simplified Zig Zag indicator.
    Returns a Series with values = price at swing points, NaN elsewhere.
    """
    zz = pd.Series(index=high.index, dtype=float)
    # Simple implementation: find local maxima/minima
    high_idx = high.rolling(depth, center=True).apply(lambda x: x.argmax() == depth//2, raw=True).astype(bool)
    low_idx = low.rolling(depth, center=True).apply(lambda x: x.argmin() == depth//2, raw=True).astype(bool)
    zz[high_idx] = high[high_idx]
    zz[low_idx] = low[low_idx]
    return zz
