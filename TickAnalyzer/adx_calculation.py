import pandas as pd
import numpy as np


def calculate_adx(data, period=14):

    # =========================================================
    # COPY DATA
    # =========================================================

    df = data.copy()

    high = df['High']
    low = df['Low']
    close = df['Close']

    # =========================================================
    # STEP 1 — TRUE RANGE (TR)
    # =========================================================

    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # =========================================================
    # STEP 2 — DIRECTIONAL MOVEMENT (+DM / -DM)
    # =========================================================

    up_move = high.diff()

    down_move = low.shift(1) - low

    plus_dm = np.where(
        (up_move > down_move) & (up_move > 0),
        up_move,
        0.0
    )

    minus_dm = np.where(
        (down_move > up_move) & (down_move > 0),
        down_move,
        0.0
    )

    plus_dm = pd.Series(plus_dm, index=df.index)
    minus_dm = pd.Series(minus_dm, index=df.index)

    # =========================================================
    # STEP 3 — WILDER SMOOTHING ATR
    # =========================================================

    atr = pd.Series(index=df.index, dtype='float64')

    # First ATR value
    atr.iloc[period - 1] = tr.iloc[:period].mean()

    # Wilder recursive smoothing
    for i in range(period, len(df)):
        atr.iloc[i] = (
            (atr.iloc[i - 1] * (period - 1))
            + tr.iloc[i]
        ) / period

    # =========================================================
    # STEP 4 — SMOOTH +DM
    # =========================================================

    plus_dm_smoothed = pd.Series(index=df.index, dtype='float64')

    plus_dm_smoothed.iloc[period - 1] = plus_dm.iloc[:period].mean()

    for i in range(period, len(df)):
        plus_dm_smoothed.iloc[i] = (
            (plus_dm_smoothed.iloc[i - 1] * (period - 1))
            + plus_dm.iloc[i]
        ) / period

    # =========================================================
    # STEP 5 — SMOOTH -DM
    # =========================================================

    minus_dm_smoothed = pd.Series(index=df.index, dtype='float64')

    minus_dm_smoothed.iloc[period - 1] = minus_dm.iloc[:period].mean()

    for i in range(period, len(df)):
        minus_dm_smoothed.iloc[i] = (
            (minus_dm_smoothed.iloc[i - 1] * (period - 1))
            + minus_dm.iloc[i]
        ) / period

    # =========================================================
    # STEP 6 — +DI AND -DI
    # =========================================================

    plus_di = 100 * (plus_dm_smoothed / atr)

    minus_di = 100 * (minus_dm_smoothed / atr)

    # =========================================================
    # STEP 7 — DX
    # =========================================================

    denominator = (plus_di + minus_di).replace(0, np.nan)

    dx = (
        (plus_di - minus_di).abs() / denominator
    ) * 100

    # =========================================================
    # STEP 8 — ADX
    # =========================================================

    adx = pd.Series(index=df.index, dtype='float64')

    # First ADX value
    adx.iloc[(period * 2) - 1] = dx.iloc[period:(period * 2)].mean()

    # Wilder recursive smoothing
    for i in range(period * 2, len(df)):
        adx.iloc[i] = (
            (adx.iloc[i - 1] * (period - 1))
            + dx.iloc[i]
        ) / period

    # =========================================================
    # FINAL OUTPUT
    # =========================================================

    result = pd.DataFrame({
        'ADX': adx,
        '+DI': plus_di,
        '-DI': minus_di
    })

    return result