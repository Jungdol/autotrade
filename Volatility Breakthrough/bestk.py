import time
import pyupbit
import numpy as np
import sys

# coin = "KRW-BTC"

coins = pyupbit.get_tickers(fiat="KRW")


def get_ror(counts, coin, k=0.5):
    # 비트코인을 기준으로 변동선 돌파 전략 중 변동폭 * k 중 좋은 k 값을 찾음
    df = pyupbit.get_ohlcv(coin, count=counts)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.05
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror


max_coin = []
max_k = []
'''
for count in range(3, 7):
    ks = []
    print("------- " + str(count) + " -------")
    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_ror(count, "KRW-STORJ", k)
        ks.append(ror)
        print("%.1f %f" % (k, ror))
    print("high k\n0." + str(ks.index(max(ks)) + 1) + " %f" % max(ks))
    time.sleep(0.5)

'''
sys.stdout = open("output.txt", 'w')

for i in range(0, len(coins)):
    tmp_ks = 0
    tmp_coins = ""
    print("---------- " + coins[i] + " ---------")
    for count in range(3, 8):
        ks = []
        k = 0
        ror = 0
        print("------- " + str(count) + " -------")
        for k in np.arange(0.1, 1.0, 0.1):
            ror = get_ror(count, coins[i], k)
            ks.append(ror)
            print("%.1f %f" % (k, ror))

        tmp = "high k\n0." + str(ks.index(max(ks)) + 1)
        print("high k\n0." + str(ks.index(max(ks)) + 1) + " %f" % max(ks))
        time.sleep(0.25)
        if count == 4:
            tmp_ks = max(ks)
            tmp_coins = coins[i]
        elif tmp_ks < max(ks):
            tmp_ks = max(ks)
            tmp_coins = coins[i]

    print("\n" + tmp_coins, tmp_ks)

print("\n" + str(coins))
print("\n" + str(len(coins)))
