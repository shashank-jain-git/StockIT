# MACD Calculation (not Commited)
def calculate_macd(close_prices, fast=12, slow=26, signal=9):
    ema_fast = close_prices.ewm(span=fast, adjust=False).mean()
    ema_slow = close_prices.ewm(span=slow, adjust=False).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    return macd_line, signal_line, histogram