import pyupbit
import numpy as np


def get_ror(k=0.5):
    #비트코인을 기준으로 변동선 돌파 전략 중 변동폭 * k 중 좋은 k 값을 찾음
    df = pyupbit.get_ohlcv("KRW-DAWN", count=7)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.05
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror


for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k)
    print("%.1f %f" % (k, ror))