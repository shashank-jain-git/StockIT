def rsi_calculation(close_prices, period=14):
    close_prices = list(close_prices)

    gains = []
    losses = []

    # Step 1: Calculate price changes
    for i in range(1, len(close_prices)):
        change = close_prices[i] - close_prices[i - 1]
        gains.append(max(change, 0))
        losses.append(abs(min(change, 0)))

    # Step 2: Initial average gain/loss
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    rsi_values = [None] * (period)

    # Step 3: Smoothed RSI calculation
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        rsi_values.append(rsi)

    # Match length with original data
    rsi_values = [None] + rsi_values

    return rsi_values