import time
import sel_for_BTC
import sel_for_ETH
import binance_BTC
import binance_ETH
from datetime import datetime

while True:
    time.sleep(10) # 계속 돌아가면 CPU 낭비이니 10초씩 휴식
    nowtime = datetime.now() #현재 시간 입력
    date = datetime.strptime(str(nowtime), "%Y-%m-%d %H:%M:%S.%f") # 현재 분 입력
    if date.minute == 29 or date.minute == 59: # 29분이나 59분일경우, 동작 시작
        BTC_w2cd_result = sel_for_BTC.run() # BTC 크롤링
        if binance_BTC.can_enter() and BTC_w2cd_result == "BUY": # BUY 판정이면서, 현재 들어간게 없으면 BTC 롱 진입
            time.sleep(40)
            binance_BTC.order_long()
        elif binance_BTC.can_enter() and BTC_w2cd_result == "SELL": #SELL 판정이면서, 현재 들어간게 없으면 BTC 숏 진입
            time.sleep(40)
            binance_BTC.order_short()

        ETH_w2cd_result = sel_for_ETH.run() # ETH 크롤링
        if binance_ETH.can_enter() and ETH_w2cd_result == "BUY": # BUY 판정이면서, 현재 들어간게 없으면 ETH 롱 진입
            time.sleep(40)
            binance_ETH.order_long()
        elif binance_ETH.can_enter() and ETH_w2cd_result == "SELL": # SELL 판정이면서, 현재 들어간게 없으면 ETH 숏 진입
            time.sleep(40)
            binance_ETH.order_short()