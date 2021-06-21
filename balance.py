import bybit
import mkdntjr12_bybit1
import datetime as dt
import time
import dateutil.parser
from pytz import timezone

def balance(coin):
    client = bybit.bybit(test=False, api_key=mkdntjr12_bybit1.api_key, api_secret=mkdntjr12_bybit1.secret_key) #mkdntjr12_bybit1.secret_key
    balance = client.Wallet.Wallet_getBalance().result()
    equity = balance[0]["result"][coin]["equity"]
    # 지갑 잔고 : equity = wallet_balance + unrealised_pnl (미실현손익)
    # print("equity : {0}".format(equity))
    available_balance = balance[0]["result"][coin]["available_balance"]
    # available_balance = wallet_balance - (position_margin + occ_closing_fee + occ_funding_fee + order_margin)
    # print("available_balance : {0}".format(available_balance))
    # used_margin = balance[0]["result"][coin]["used_margin"]
    # print("used_margin : {0}".format(used_margin))
    # order_margin = balance[0]["result"][coin]["order_margin"]
    # 주문 시 사용한 마진?? 뜻을 좀 알아두자 
    # print("order_margin : {0}".format(order_margin))
    # position_margin = balance[0]["result"][coin]["position_margin"]
    # print("position_margin : {0}".format(position_margin))
    # occ_closing_fee = balance[0]["result"][coin]["occ_closing_fee"]
    # print("occ_closing_fee : {0}".format(occ_closing_fee))
    # occ_funding_fee = balance[0]["result"][coin]["occ_funding_fee"]
    # print("occ_funding_fee : {0}".format(occ_funding_fee))
    wallet_balance = balance[0]["result"][coin]["wallet_balance"]
    # 현재 지갑에 남아있는 잔액
    # print("wallet_balance : {0}".format(wallet_balance))
    realised_pnl = balance[0]["result"][coin]["realised_pnl"]
    # 오늘의 실현 손익
    # print("realised_pnl : {0}".format(realised_pnl))
    unrealised_pnl = balance[0]["result"][coin]["unrealised_pnl"]
    # 미실현 손익 : 포지션을 잡을 때만 나타나는 듯?
    # print("unrealised_pnl : {0}".format(unrealised_pnl))
    # cum_realised_pnl = balance[0]["result"][coin]["cum_realised_pnl"]
    # print("cum_realised_pnl : {0}".format(cum_realised_pnl))
    # given_cash = balance[0]["result"][coin]["given_cash"]
    # print("given_cash : {0}".format(given_cash))
    # service_cash = balance[0]["result"][coin]["service_cash"]
    # print("service_cash : {0}".format(service_cash))
    # print("현재 자산 : {0} , 가용 ".format(equity) + coin + " 잔고 : {0} , 지갑 잔고 : {1} , 미실현손익 : {2} , 실현손익 : {3} ".format(available_balance, wallet_balance, unrealised_pnl,realised_pnl))
    return coin, equity, available_balance, wallet_balance, unrealised_pnl, realised_pnl

'''
#예시
#coin, equity, available_balance, wallet_balance, unrealised_pnl, realised_pnl
balance = balance("BTC")
mybal_coin = balance[0]
mybal_equity = balance[1]
mybal_available_balance = balance[2]
mybal_wallet_balance = balance[3]
mybal_unrealised_pnl = balance[4]
mybal_realised_pnl = balance[5]
print("현재 자산 : {0} , 가용 ".format(mybal_equity) + mybal_coin + " 잔고 : {0} , 지갑 잔고 : {1} , 미실현손익 : {2} , 실현손익 : {3} ".format(mybal_available_balance, mybal_wallet_balance, mybal_unrealised_pnl,mybal_realised_pnl))
'''

def position(market):
    client = bybit.bybit(test=False, api_key=mkdntjr12_bybit1.api_key, api_secret=mkdntjr12_bybit1.secret_key) #mkdntjr12_bybit1.secret_key
    myposition = client.Positions.Positions_myPosition(symbol=market).result()[0]["result"]
    time = client.Market.Market_orderbook(symbol=market).result()
    now = float(time[0]["time_now"]) #한국 시간을 보여줌
    myposi_side = myposition["side"] #공매도 공매수
    myposi_size = myposition["size"] #포지션 사이즈
    myposi_leverage = myposition["leverage"] #포지션 레버리지
    myposi_iso = myposition["is_isolated"] #true 면 격리, false 면 격차 - 보통 격리로 할 듯
    myposi_ent_price = myposition["entry_price"] #진입 가격
    myposi_liq_price = myposition["liq_price"] #청산 가격
    myposi_realised_pnl = myposition["realised_pnl"] #현 포지션 실현 손익 (펀딩비 손익)
    myposi_unrealised_pnl = myposition["unrealised_pnl"] #미실현 손익
    myposi_time = myposition["updated_at"] #date 형식이 타임존에 맞게 되어 있음
    yourdate = dateutil.parser.parse(myposi_time) #UTC 시간으로 내 주문 시간
    myposi_timestamp = dt.datetime.timestamp(yourdate) #주문일자와 현재의 차이를 확인하기 위한 것
    KST_myposi = yourdate.astimezone(timezone("Asia/Seoul")) #한국 시간으로 주문 시간
    time_delta = round(((now - round(myposi_timestamp))/3600),2) #주문시간과 현시간의 차이 - 시간으로 표기
    # print("시장 : {0} , 공매수/공매도 : {1} , 계약 수량 : {2} , 레버리지 : {3} , 격리(T)/교차(F) : {4} , 진입가 : {5} , 청산 예상가 : {6} ".format(market,myposi_side,myposi_size,myposi_leverage,myposi_iso,myposi_ent_price,myposi_liq_price))
    # print("진입 시간 : {0} , 보유 기간 : {1}시간 , 미실현 손익 : {2} , 실현 손익 : {3} ".format(KST_myposi,time_delta,myposi_unrealised_pnl,myposi_realised_pnl))
    return market, myposi_side, myposi_size, myposi_leverage, myposi_iso, myposi_ent_price, myposi_liq_price, myposi_realised_pnl, myposi_unrealised_pnl, KST_myposi, time_delta

'''
#예시
#market, myposi_side, myposi_size, myposi_leverage, myposi_iso, myposi_ent_price, myposi_liq_price, myposi_realised_pnl, myposi_unrealised_pnl, KST_myposi, time_delta
position = position("BTCUSD")
myposi_market = position[0]
myposi_side = position[1]
myposi_size = position[2]
myposi_leverage = position[3]
myposi_iso = position[4]
myposi_ent_price = position[5]
myposi_liq_price = position[6]
myposi_realised_pnl = position[7]
myposi_unrealised_pnl = position[8]
KST_myposi = position[9]
time_delta = position[10]
print("시장 : {0} , 공매수/공매도 : {1} , 계약 수량 : {2} , 레버리지 : {3} , 격리(T)/교차(F) : {4} , 진입가 : {5} , 청산 예상가 : {6} ".format(myposi_market,myposi_side,myposi_size,myposi_leverage,myposi_iso,myposi_ent_price,myposi_liq_price))
print("진입 시간 : {0} , 보유 기간 : {1}시간 , 미실현 손익 : {2} , 실현 손익 : {3} ".format(KST_myposi,time_delta,myposi_unrealised_pnl,myposi_realised_pnl))
'''