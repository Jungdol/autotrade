import pyupbit
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import pandas as pd


def get_ohlcv(ticker):
    dfs = []
    # 조회할 코인, 일봉 또는 분봉으로 조회, 적힌 날짜, 시간까지 200개의 데이터 조회
    # df = pyupbit.get_ohlcv(ticker, interval="minute1", to="20210423 11:00:00")
    df = pyupbit.get_ohlcv(ticker, interval="minute1", to="20210414 23:00:00")
    # OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량

    for i in range(60):
        df = pyupbit.get_ohlcv(ticker, interval="minute1", to=df.index[0])  # 과거 데이터 200개 조회
        dfs.append(df)
        time.sleep(0.2)

    df = pd.concat(dfs)
    df = df.sort_index()
    return df


def short_trading_for_1per(df):
    # 이동 평균선 (급락으로 인해 120분 이동 평균선도 적용)
    ma15 = df['close'].rolling(15).mean().shift(1)
    ma50 = df['close'].rolling(50).mean().shift(1)
    ma120 = df['close'].rolling(120).mean().shift(1)

    # 1. 매수 일자 판별
    cond_0 = df['high'] >= df['open'] * 1.01  # df의 고가가 df 시가 대비 1프로 상승 시 매수
    cond_1 = (ma15 >= ma50) & (ma15 <= ma50 * 1.03)
    cond_2 = ma50 > ma120
    cond_buy = cond_0 & cond_1 & cond_2

    acc_ror = 1  # 전체 수익률 저장 함수
    sell_date = None

    ax_ror = []
    ay_ror = []

    # 2. 매도 조건 탐색 및 수익률 계산

    # 반복문을 사용하여 선택된 날짜를 하나씩 가져옴
    for buy_date in df.index[cond_buy]:
        if sell_date != None and buy_date <= sell_date:
            continue
        target = df.loc[buy_date:]  # buy_date 부터 끝까지의 데이터 가져옴

        cond = target['high'] >= df.loc[buy_date, 'open'] * 1.02  # target 의 고가가 target 의 시가에서 2프로 상승 시 매도
        sell_candidate = target.index[cond]  # index 에는 날짜 정보가 저장되어 있음.

        # 만약 매도할 수 있는 날짜가 존재하지 않을 시 공가 데이터 매도, 탐색 중지
        if len(sell_candidate) == 0:
            buy_price = df.loc[buy_date, 'open'] * 1.01  # buy_price 는 매수한 시간 정보(행) , 시가(열) 에서 1프로 상승
            sell_price = df.iloc[-1, 3]  # sell_price 는 마지막 행, 종가(3)
            acc_ror *= (sell_price / buy_price)
            ax_ror.append(df.index[-1])
            ay_ror.append(acc_ror)
            break
        else:
            sell_date = sell_candidate[0]
            acc_ror *= 1.001
            ax_ror.append(sell_date)
            ay_ror.append(acc_ror)
            # 수수료 0.005 + 슬리피지 0.004
            # 1.01 - (수수료 + 슬리피지)

    ''' 주석 처리부분은 그래프로 시각화 하게 만드는 부분임임
    candle= go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
    )

    ror_chart = go.Scatter(
        x=ax_ror,
        y=ay_ror
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(candle)
    fig.add_trace(ror_chart, secondary_y=True)

    for idx in df.index[cond_buy]:
        fig.add_annotation(
            x=idx,
            y=df.loc[idx, 'open']
        )
    fig.show()
    '''
    return acc_ror

'''
# 이 부분은 데이터 로딩이 오래걸려 따로 엑셀문서로 만드는 부분
for ticker in ["KRW-BTC", "KRW-LTC", "KRW-ETH", "KRW-ADA"]:
    df = get_ohlcv(ticker)
    df.to_excel(f"{ticker}.xlsx")
'''

for ticker in ["KRW-BTC", "KRW-LTC", "KRW-ETH", "KRW-ADA"]:
# for ticker in ["KRW-LTC"]:  # LTC 가 급락으로 인해 수익률도 같이 떨어져 테스트 용으로 사용했음
    df = pd.read_excel(f"{ticker}.xlsx", index_col=0)
    ror = short_trading_for_1per(df)
    periodYield = df.iloc[-1, 3] / df.iloc[0, 0]  # 기간 수익률

    print(ticker, f"{ror:.2f}", f"{periodYield:.2f}")
