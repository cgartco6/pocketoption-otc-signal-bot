import unittest
import pandas as pd
from signals.strategy import detect_signals

class TestStrategy(unittest.TestCase):
    def test_detect_signals_returns_tuple(self):
        df = pd.DataFrame({
            'Open': [1.1]*100,
            'High': [1.2]*100,
            'Low': [1.0]*100,
            'Close': [1.15]*100
        })
        pre, main = detect_signals(df)
        self.assertIn(pre, [None, 'BUY_SETUP', 'SELL_SETUP'])
        self.assertIn(main, [None, 'BUY', 'SELL'])

if __name__ == '__main__':
    unittest.main()
