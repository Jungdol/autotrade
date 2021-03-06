import pyupbit
import numpy as np

coin = "KRW-COIN"
k = 0.5

# OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량 / count 는 날짜
df = pyupbit.get_ohlcv(coin, count=7)
# 변동폭 * k 계산, (고가 - 저가) * k값
df['range'] = (df['high'] - df['low']) * k
# target(매구사), range 컬럼을 한 칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)
# 수수료
fee = 0.05

# ror(수익), np.where(조건문, 참일 때 값, 거짓일 때 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)

# 누적 곱 계산(cumprod) -> 누적 수익률
df['hpr'] = df['ror'].cumprod()
# Draw Down 게산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
# MDD 계산
print("MDD(%): ", df['dd'].max())
# 엑셀로 출력
df.to_excel(coin + ".xlsx")
