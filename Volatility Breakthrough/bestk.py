import time
import pyupbit
import numpy as np
import pandas as pd
import sys

# coin = "KRW-BTC"

coins = pyupbit.get_tickers(fiat="KRW")

nowTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))


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


def allCoins():
    print("데이터 수집, 작성 시작합니다.")
    global dfs
    data = []
    ks = []
    rors = []
    for i in range(0, len(coins)):
        print(str(coins[i]) + " 데이터 수집 중")
        for count in range(3, 8):
            print(str(count)+"일 전 데이터 작성 중")
            dfCoins = coins[i]
            days = count
            for k in np.arange(0.1, 1.0, 0.1):
                ror = get_ror(count, coins[i], k)
                ks.append(k)
                rors.append(ror)
                data.append([dfCoins, days, k, ror])

            time.sleep(0.2)
        print(str(coins[i]) + " 작업 완료\n")
        dfs = pd.DataFrame(data, columns=['CoinName', 'Days', 'k값', '수익'])

    print("모든 작업 완료")
    return dfs


allCoins().to_excel(str(nowTime)+" upbit Coins.xlsx", index=False)
