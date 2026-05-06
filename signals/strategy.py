import pandas as pd
from indicators.ma import moving_average
from indicators.rsi import rsi
from indicators.supertrend import supertrend
from indicators.zigzag import zigzag
from config.settings import MA_PERIOD, RSI_PERIOD, SUPERTREND_PERIOD, SUPERTREND_MULTIPLIER

def detect_signals(df: pd.DataFrame):
    """
    Returns: (pre_signal, main_signal)
    pre_signal: 'BUY_SETUP', 'SELL_SETUP', or None
    main_signal: 'BUY', 'SELL', or None
    """
    # 1. Calculate indicators
    df['MA'] = moving_average(df['Close'], MA_PERIOD)
    df['RSI'] = rsi(df['Close'], RSI_PERIOD)
    df['ST'], df['ST_Direction'] = supertrend(df, SUPERTREND_PERIOD, SUPERTREND_MULTIPLIER)
    df['ZZ'] = zigzag(df['High'], df['Low'], depth=12, deviation=5, backstep=3)
    
    # 2. Latest values
    last = df.iloc[-1]
    prev2 = df.iloc[-3]  # 2 candles ago for 3‑min confirmation
    last_zz = df['ZZ'].dropna().iloc[-1] if not df['ZZ'].dropna().empty else None
    
    # 3‑min confirmation: conditions must hold for at least 3 consecutive candles
    buy_confirmed = all(
        (df['Close'].iloc[-i] > df['MA'].iloc[-i]) and
        (df['RSI'].iloc[-i] > 50) and
        (df['ST_Direction'].iloc[-i] == 1)
        for i in range(1, 4)
    )
    sell_confirmed = all(
        (df['Close'].iloc[-i] < df['MA'].iloc[-i]) and
        (df['RSI'].iloc[-i] < 50) and
        (df['ST_Direction'].iloc[-i] == -1)
        for i in range(1, 4)
    )
    
    # --- MAIN SIGNALS (Katie's full entry) ---
    main_buy = buy_confirmed and (last_zz is not None and last_zz < last['Close'])
    main_sell = sell_confirmed and (last_zz is not None and last_zz > last['Close'])
    
    # --- PRE‑SIGNALS (early warning) ---
    pre_buy = (
        (last['Close'] > last['MA']) and
        (last['RSI'] > 50) and
        not buy_confirmed   # not yet fully aligned for 3 minutes
    )
    pre_sell = (
        (last['Close'] < last['MA']) and
        (last['RSI'] < 50) and
        not sell_confirmed
    )
    
    pre_signal = None
    if pre_buy:
        pre_signal = 'BUY_SETUP'
    elif pre_sell:
        pre_signal = 'SELL_SETUP'
    
    main_signal = None
    if main_buy:
        main_signal = 'BUY'
    elif main_sell:
        main_signal = 'SELL'
    
    return pre_signal, main_signal
