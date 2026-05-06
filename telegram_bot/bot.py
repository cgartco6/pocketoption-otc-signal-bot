import os
import logging
from telegram import Bot, ParseMode
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = Bot(token=BOT_TOKEN)

def send_setup(pair, signal_type, price, ma, rsi, st_direction, timestamp):
    direction = "POTENTIAL LONG" if signal_type == 'BUY_SETUP' else "POTENTIAL SHORT"
    color = "🟡" if signal_type == 'BUY_SETUP' else "🟠"
    
    msg = f"""
{color} *SETUP ALERT* {color}
📌 *{pair}* – {direction}

💵 *Price:* {price:.5f}
📈 *MA(20):* {ma:.5f}
⚡ *RSI(14):* {rsi:.1f}
📊 *Supertrend:* {'GREEN' if st_direction == 1 else 'RED'}
⏰ *Time:* {timestamp}

⚠️ Conditions are partially met. Watch for 3‑minute confirmation.
    """
    try:
        bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logging.error(f"Setup send failed: {e}")

def send_main_signal(pair, signal_type, price, ma, rsi, st_direction, timestamp):
    emoji = '🟢' if signal_type == 'BUY' else '🔴'
    direction = 'ENTER LONG 🔼' if signal_type == 'BUY' else 'ENTER SHORT 🔽'
    
    msg = f"""
{emoji} *SIGNAL: {signal_type} {pair}* {emoji}

📊 *Direction:* {direction}
💵 *Entry Price:* {price:.5f}
📈 *MA(20):* {ma:.5f}
⚡ *RSI(14):* {rsi:.1f}
📊 *Supertrend:* {'GREEN' if st_direction == 1 else 'RED'}
⏰ *Time:* {timestamp}

⚠️ High risk – no stop loss used (per Katie's method).
    """
    try:
        bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.MARKDOWN)
        logging.info(f"Main signal sent: {signal_type} {pair}")
    except Exception as e:
        logging.error(f"Main signal send failed: {e}")
