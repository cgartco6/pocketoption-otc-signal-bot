import pandas as pd
from data.market_data import get_1min_data
from signals.strategy import detect_signals

def backtest(pair: str, days: int = 7):
    data = get_1min_data(pair, bars=days*24*60)
    signals = []
    for i in range(50, len(data)):
        df_slice = data.iloc[:i+1]
        pre, main = detect_signals(df_slice)
        if main:
            signals.append((data.index[i], main, data['Close'].iloc[i]))
    print(f"Backtest on {pair}: {len(signals)} signals found")
    return signals

if __name__ == '__main__':
    backtest('EURUSD=X')
