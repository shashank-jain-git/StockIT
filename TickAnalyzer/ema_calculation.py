def calculate_ema(close_prices, period=20):
    close_prices = list(close_prices)
    ema_values = []

    k = 2 / (period + 1)

    # Step 1: First EMA = SMA
    sma = sum(close_prices[:period]) / period
    ema_values = [None] * (period - 1)  # first values undefined
    ema_values.append(sma)

    # Step 2: EMA calculation
    for price in close_prices[period:]:
        prev_ema = ema_values[-1]
        ema = (price * k) + (prev_ema * (1 - k))
        ema_values.append(ema)

    return ema_values