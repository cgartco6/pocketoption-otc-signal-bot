import time
import logging
from datetime import datetime
from config.settings import MAJOR_PAIRS, MINUTE_INTERVAL
from data.market_data import get_1min_data
from signals.strategy import detect_signals
from telegram_bot.bot import send_setup, send_main_signal

last_pre_signal = {}

def run_signal_loop():
    logging.basicConfig(level=logging.INFO)
    
    while True:
        for pair in MAJOR_PAIRS:
            try:
                df = get_1min_data(pair, bars=100)
                pre_signal, main_signal = detect_signals(df)
                
                if pre_signal and last_pre_signal.get(pair) != pre_signal:
                    last = df.iloc[-1]
                    send_setup(
                        pair=pair.replace('=X',''),
                        signal_type=pre_signal,
                        price=last['Close'],
                        ma=last['MA'],
                        rsi=last['RSI'],
                        st_direction=last['ST_Direction'],
                        timestamp=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
                    )
                    last_pre_signal[pair] = pre_signal
                elif not pre_signal:
                    last_pre_signal[pair] = None
                
                if main_signal:
                    last = df.iloc[-1]
                    send_main_signal(
                        pair=pair.replace('=X',''),
                        signal_type=main_signal,
                        price=last['Close'],
                        ma=last['MA'],
                        rsi=last['RSI'],
                        st_direction=last['ST_Direction'],
                        timestamp=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
                    )
            except Exception as e:
                logging.error(f"Error processing {pair}: {e}")
        
        time.sleep(MINUTE_INTERVAL)

if __name__ == '__main__':
    run_signal_loop()
