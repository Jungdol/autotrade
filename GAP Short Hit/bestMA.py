# 비공개
# 원리 : 상승장, 하락장 때 이동 평균선을 값을 변경하여 각각의 최적의 이동 평균선 저장 후 출력
# backtest.py 의 값 : ma15, ma50, ma120
# ma15와 ma50을 비교하여 ma15가 ma50보다 높으면 (이격도를 보고) 상승세로 파악 후 매수, 1퍼가 오르면 매도
# backtest.py 코드 값을 조금 개조하여 최적의 이동 평균선을 찾는다.
