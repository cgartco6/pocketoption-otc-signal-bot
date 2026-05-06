# Trading configuration
MA_PERIOD = 20
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
SUPERTREND_PERIOD = 10
SUPERTREND_MULTIPLIER = 3.0

# Major forex pairs (Pocketoption OTC)
MAJOR_PAIRS = [
    'EURUSD=X', 'GBPUSD=X', 'USDJPY=X',
    'AUDUSD=X', 'USDCAD=X', 'NZDUSD=X',
    'USDCHF=X'
]

# Signal timing
MINUTE_INTERVAL = 60          # seconds between checks
CONFIRMATION_BARS = 3         # Katie's 3‑minute confirmation rule
