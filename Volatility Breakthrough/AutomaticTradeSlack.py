import time
import pyupbit
import datetime
import requests

with open("upbit.txt", "r") as f:
    key0 = f.readline().strip()
    key1 = f.readline().strip()

myToken = "xoxp-token"


def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": text}
                             )


def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15


def get_balance(coin):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == coin:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


coinName = "COIN"
tradingCoin = "KRW-COIN"
k = 0.1

slackChannel = "변동성-전략"

inBuy = True  # 한 번만 매수하기 위함

# 로그인
upbit = pyupbit.Upbit(key0, key1)

# 우리나라 화폐, 암호화폐 생성
krw = upbit.get_balance("KRW")
coins = upbit.get_balance(coinName)

# 얼마나 파는 지, 얼마나 사는 지 설정
buyValue = krw * 0.9995  # 0.9995 인 이유는 수수료 0.005% 때문이다.
sellValue = coins * 0.9995

# 시작 메세지 슬랙 전송
print("Autotrade start")
post_message(myToken, slackChannel, "변동성 돌파 전략으로 자동매매 시작\n매수, 매도 코인 : " + str(coinName) + " " + "k값 : " + str(k))

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(tradingCoin)  # 오전 9시
        end_time = start_time + datetime.timedelta(days=1)  # 오전 9시 + 1일
        print(now)

        # 오전 9시 < 현재 < 8시 59분 50초
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(tradingCoin, k)
            ma15 = get_ma15(tradingCoin)
            current_price = get_current_price(tradingCoin)

            if target_price < current_price and ma15 < current_price:

                if krw > 5000 and inBuy == True:  # 최소 거래 금액인 5천원 이상이면
                    buy_result = upbit.buy_market_order(tradingCoin, buyValue)  # buyValue 값만큼 매수
                    post_message(myToken, slackChannel, str(coinName) + " buy : " + str(buy_result))
                    inBuy = False  # 매수 후 False 로 매수 안되게 함

        else:
            if coins > (5000 / get_current_price(tradingCoin)):  # 코인 최소 거래 금액 5천원 이상이면
                sell_result = upbit.sell_market_order(tradingCoin, sellValue)  # buyValue 값만큼 매도
                post_message(myToken, slackChannel, str(coinName) + " sell : " + str(sell_result))
                inBuy = True  # 매도 후 True 로 9시에 다시 매수
        time.sleep(1)
    except Exception as e:
        print(e)
        post_message(myToken, slackChannel, e)
        time.sleep(1)
