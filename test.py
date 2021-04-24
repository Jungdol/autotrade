import pyupbit

access = "4xlvn5ZJj0Z58Kvx07GOJbQg9wUBFtPBLbjqjHxS"  # 본인 값으로 변경
secret = "efO7jZS5eqxIvh6Z0mK6Gn1esbQH3YqjehPGMhx7"  # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-XRP"))  # KRW-XRP 조회
print(upbit.get_balance("KRW"))  # 보유 현금 조회
