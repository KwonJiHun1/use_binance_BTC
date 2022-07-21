import ccxt
import pprint
import time
import datetime
import pandas as pd
import larry
import math

def can_enter(): # 현재 진입되어있는게 있는지 체크
    with open("api.txt") as f:  ##################       api
        lines = f.readlines()
        api_key = lines[0].strip()
        secret = lines[1].strip()

        # binance 객체 생성
    binance = ccxt.binance(config={
        'apiKey': api_key,
        'secret': secret,
        'enableRateLimit': True,
    })

    balance = binance.fetch_balance(params={"type": "future"})
    return balance['USDT']['used'] == 0.0


def cal_amount(usdt_balance, cur_price):  # 구매 할 갯수 지정하기
    portion = 0.98  # 현재 지갑의 몇%를 넣을것인가?
    usdt_trade = usdt_balance * portion
    amount = math.floor((usdt_trade * 1000000) / cur_price) / 1000000
    return amount

def order_long():
    with open("api2.txt") as f:  ##################     api
        lines = f.readlines()
        api_key = lines[0].strip()
        secret = lines[1].strip()

    binance = ccxt.binance(config={  # 바이낸스 객체 생성
        'apiKey': api_key,
        'secret': secret,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future'
        }
    })

    symbol = "ETH/USDT"  # ETH에 진입할것
    long_target, short_target = larry.cal_target(binance, symbol)
    balance = binance.fetch_balance()
    usdt = balance['total']['USDT']
    op_mode = False
    position = {
        "type": None,
        "amount": 0
    }
    ticker = binance.fetch_ticker(symbol)
    cur_price = ticker['last']  # 현재가

    amount = cal_amount(usdt, cur_price)

    market = binance.market(symbol)
    leverage = 10  # 래버리지 몇배?

    resp = binance.fapiPrivate_post_leverage({  # 설정한 래버리지 세팅
        'symbol': market['id'],
        'leverage': leverage
    })

    # balance = binance.fetch_balance(params={"type": "future"}) # 잔고조회
    # print(balance['USDT'])

    orders = [None] * 3
    price = cur_price
    # limit price                           ############주문 넣기
    orders[0] = binance.create_order(
        symbol=symbol,
        type="MARKET",
        side="buy",
        amount=amount,
    )
    # take profit
    orders[1] = binance.create_order(
        symbol=symbol,
        type="TAKE_PROFIT_MARKET",
        side="sell",
        amount=amount,
        params={'stopPrice': cur_price * 1.005}
    )
    # stop loss
    orders[2] = binance.create_order(
        symbol=symbol,
        type="STOP_MARKET",
        side="sell",
        amount=amount,
        params={'stopPrice': cur_price * 0.996}
    )

    for order in orders:
        pprint.pprint(order)


def order_short():
    with open("api.txt") as f:  ##################     api
        lines = f.readlines()
        api_key = lines[0].strip()
        secret = lines[1].strip()

    binance = ccxt.binance(config={  # 바이낸스 객체 생성
        'apiKey': api_key,
        'secret': secret,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future'
        }
    })

    symbol = "ETH/USDT"  # ETH에 진입할것
    long_target, short_target = larry.cal_target(binance, symbol)
    balance = binance.fetch_balance()
    usdt = balance['total']['USDT']
    op_mode = False
    position = {
        "type": None,
        "amount": 0
    }

    def cal_amount(usdt_balance, cur_price):  # 구매 할 갯수 지정하기
        portion = 0.98  # 현재 지갑의 몇%를 넣을것인가?
        usdt_trade = usdt_balance * portion
        amount = math.floor((usdt_trade * 1000000) / cur_price) / 1000000
        return amount

    ticker = binance.fetch_ticker(symbol)
    cur_price = ticker['last']  # 현재가

    amount = cal_amount(usdt, cur_price)

    market = binance.market(symbol)
    leverage = 10  # 래버리지 몇배?

    resp = binance.fapiPrivate_post_leverage({  # 설정한 래버리지 세팅
        'symbol': market['id'],
        'leverage': leverage
    })

    # balance = binance.fetch_balance(params={"type": "future"}) # 잔고조회
    # print(balance['USDT'])

    orders = [None] * 3
    price = cur_price
    # limit price                           ############주문 넣기
    orders[0] = binance.create_order(
        symbol=symbol,
        type="MARKET",
        side="sell",
        amount=amount,
    )
    # take profit
    orders[1] = binance.create_order(
        symbol=symbol,
        type="TAKE_PROFIT_MARKET",
        side="buy",
        amount=amount,
        # price=price,
        params={'stopPrice': cur_price * 0.995}
    )
    # stop loss
    orders[2] = binance.create_order(
        symbol=symbol,
        type="STOP_MARKET",
        side="buy",
        amount=amount,
        # price=price,
        params={'stopPrice': cur_price * 1.004}
    )

    for order in orders:
        pprint.pprint(order)