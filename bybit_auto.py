import bybit
import time
import datetime
# import mkdntjr12_bybit1
import pandas as pd
import balance as bl
import order
import ohlcv
import rsi
import math


client = bybit.bybit(test=False, api_key="Ny2IKnIE8QuRYRSrlG", api_secret="a1ULO7ygdDG9kYXDtz2MkAaTPdcWr7SwEXum")
info = client.Market.Market_symbolInfo(symbol="BTCUSD").result() # 마켓에서 거래되는 모든 거래쌍에 대한 현재 정보를 가져오는 것 keys 에 info 를 넣고 for i 문을 통해 안에 뭐가 들어있는지 확인이 가능함


#로그인 이후 간단한 정보 기입, 24시간 관련 정보 기입 필요
print("로그인")
# print("BTCUSD 이번 펀딩 rate : {0}%".format(100*float(info[0]["result"][0]["funding_rate"])))
# print("BTCUSD 다음 펀딩 rate : {0}%".format(100*float(info[0]["result"][0]["predicted_funding_rate"])))
print("BTCUSD 이번 펀딩 rate : {0}%".format(round(100*float(info[0]["result"][0]["funding_rate"]),4)))            #너무 복잡하니까 펀딩비 소수점으로 바꿔버리기
print("BTCUSD 다음 펀딩 rate : {0}%".format(round(100*float(info[0]["result"][0]["predicted_funding_rate"]),4)))  #너무 복잡하니까 펀딩비 소수점으로 바꿔버리기

#잔고 표시
print("현재 자산")
#coin, equity, available_balance, wallet_balance, unrealised_pnl, realised_pnl
balance = bl.balance("BTC")
mybal_coin = balance[0]
mybal_equity = balance[1]
mybal_available_balance = balance[2]
mybal_wallet_balance = balance[3]
mybal_unrealised_pnl = balance[4]
mybal_realised_pnl = balance[5]
print("현재 자산 : {0} , 가용 ".format(mybal_equity) + mybal_coin + " 잔고 : {0} , 지갑 잔고 : {1} , 미실현손익 : {2} , 실현손익 : {3} ".format(mybal_available_balance, mybal_wallet_balance, mybal_unrealised_pnl,mybal_realised_pnl))

#현재 포지션 표시
#market, myposi_side, myposi_size, myposi_leverage, myposi_iso, myposi_ent_price, myposi_liq_price, myposi_realised_pnl, myposi_unrealised_pnl, KST_myposi, time_delta
print("현재 포지션")
position = bl.position("BTCUSD")
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

#ohlcv data 가져오기
df1 = ohlcv.ohlcv() #ohlcv data 를 가져와 df1 에 저장
df2 = rsi.rsi(df1,14)
df2 = df2.sort_values(by="open_time" , ascending=False)
cur_RSI = df2.iloc[0]["RSI"] #마지막 10분 봉 기준의 RSI 값을 저장
print("현재 RSI 값 : {0}".format(cur_RSI))
# print(info[0]["result"][0]["last_price"]) #현재의 마지막 거래 가격
'''

while True:
    time.sleep(5)
    #ohlcv data 가져오기
    df1 = ohlcv.ohlcv() #ohlcv data 를 가져와 df1 에 저장
    df2 = rsi.rsi(df1,14)
    df2 = df2.sort_values(by="open_time" , ascending=False)
    cur_RSI = df2.iloc[0]["RSI"] #마지막 10분 봉 기준의 RSI 값을 저장
    cur_time = df2.index[0]
    cur_info = bl.position("BTCUSD") #현재 내 포지션 정보를 cur_info 에 저장
    cur_side = cur_info[1]
    cur_size = cur_info[2]
    print("현재 RSI 값 : {0}".format(cur_RSI))
    if cur_RSI <=21:
        while True:
            time.sleep(5)
            df1 = ohlcv.ohlcv() #ohlcv data 를 가져와 df1 에 저장
            df2 = rsi.rsi(df1,14)
            df2 = df2.sort_values(by="open_time" , ascending=False)
            new_time = df2.index[0]
            if new_time == cur_time: #업데이트 되기 전까지는 그냥 pass
                new_RSI = cur_RSI
                print("10분 아직 안 지남")
                pass
            else: #업데이트 되면 else로 넘어가서 새로운 rsi 값을 가지게 됨
                new_RSI = df2.iloc[0]["RSI"] #마지막 새로운 RSI 값을 기입
                print("새로운 RSI 값 : {0}".format(new_RSI))

            if new_RSI > 21:
                if cur_side == "Buy":
                    print("이미 {0} 상태로 포지션 변경 없음 While 문 break".format(cur_side))
                    break
                elif cur_side == "Sell": #포지션 변경 , 자기자본율 100%
                    #이 함수가 한 번에 체결이 안될 수 있으므로, 반복문을 통해 사용 해야 함. while true 와 break 사용 필요
                    info = client.Market.Market_symbolInfo(symbol="BTCUSD").result() #현재 가격 정보를 가져오기 위한 info 함수 사용
                    last_price = info[0]["result"][0]["last_price"] #현재 가격에 대한 정보 가져오기
                    order.order("Buy",cur_size) #현재 가지고 있는 공매도 포지션 청산
                    avail_size = bl.balance("BTC")[2] #매도 이후 현재 가용자산 BTC 기준
                    avail_size = avail_size * 1 #현재 자기자본율의 100% 를 사용하겠다는 뜻 , 50% 라면 0.5로 수정 필요
                    order_size = math.floor(avail_size * math.floor(float(last_price))*0.99) #order size 는 USD 기준으로 표기해야하니 avail_size(BTC) * last price USD/BTC 적용, 0.99% 는 수수료를 위해 1% 마진
                    order.order("Buy",order_size) #가용 자산 만큼 풀 매수 이 때 위에서 버림으로 order_size 를 int 형으로 만들어줌
                    break
                else:
                    #이 함수가 한 번에 체결이 안될 수 있으므로, 반복문을 통해 사용 해야 함. while true 와 break 사용 필요
                    info = client.Market.Market_symbolInfo(symbol="BTCUSD").result() #현재 가격 정보를 가져오기 위한 info 함수 사용
                    last_price = info[0]["result"][0]["last_price"] #현재 가격에 대한 정보 가져오기
                    avail_size = bl.balance("BTC")[2] #현재 가용자산
                    avail_size = avail_size * 1 #현재 자기자본율의 100% 를 사용하겠다는 뜻 , 50% 라면 0.5로 수정 필요
                    order_size = math.floor(avail_size * math.floor(float(last_price))*0.99) #order size 는 USD 기준으로 표기해야하니 avail_size(BTC) * last price USD/BTC 적용, 0.99% 는 수수료를 위해 1% 마진
                    order.order("Buy",order_size) #가용 자산 만큼 풀 매수 이 때 위에서 버림으로 order_size 를 int 형으로 만들어줌
                    break
            else:
                pass
    elif cur_RSI >= 70:
        while True:
            time.sleep(5)
            df1 = ohlcv.ohlcv() #ohlcv data 를 가져와 df1 에 저장
            df2 = rsi.rsi(df1,14)
            df2 = df2.sort_values(by="open_time" , ascending=False)
            new_time = df2.index[0]
            if new_time == cur_time: #업데이트 되기 전까지는 그냥 pass
                new_RSI = cur_RSI
                print("10분 아직 안 지남")
                pass
            else: #업데이트 되면 else로 넘어가서 새로운 rsi 값을 가지게 됨
                new_RSI = df2.iloc[0]["RSI"] #마지막 새로운 RSI 값을 기입
                print("새로운 RSI 값 : {0}".format(new_RSI))

            if new_RSI < 70:
                if cur_side == "Sell":
                    print("이미 {0} 상태로 포지션 변경 없음 While 문 break".format(cur_side))
                    break
                elif cur_side == "Buy": #포지션 변경 , 자기자본율 100%
                    #이 함수가 한 번에 체결이 안될 수 있으므로, 반복문을 통해 사용 해야 함. while true 와 break 사용 필요
                    info = client.Market.Market_symbolInfo(symbol="BTCUSD").result() #현재 가격 정보를 가져오기 위한 info 함수 사용
                    last_price = info[0]["result"][0]["last_price"] #현재 가격에 대한 정보 가져오기
                    order.order("Sell",cur_size) #현재 가지고 있는 포지션 청산
                    avail_size = bl.balance("BTC")[2] #청산 이후 현재 가용자산 BTC 기준
                    avail_size = avail_size * 1 #현재 자기자본율의 100% 를 사용하겠다는 뜻 , 50% 라면 0.5로 수정 필요
                    order_size = math.floor(avail_size * math.floor(float(last_price))*0.99) #order size 는 USD 기준으로 표기해야하니 avail_size(BTC) * last price USD/BTC 적용, 0.99% 는 수수료를 위해 1% 마진
                    order.order("Sell",order_size) #가용 자산 만큼 풀 매수 이 때 위에서 버림으로 order_size 를 int 형으로 만들어줌
                    break
                else:
                    #이 함수가 한 번에 체결이 안될 수 있으므로, 반복문을 통해 사용 해야 함. while true 와 break 사용 필요
                    info = client.Market.Market_symbolInfo(symbol="BTCUSD").result() #현재 가격 정보를 가져오기 위한 info 함수 사용
                    last_price = info[0]["result"][0]["last_price"] #현재 가격에 대한 정보 가져오기
                    avail_size = bl.balance("BTC")[2] #현재 가용자산 BTC 기준
                    avail_size = avail_size * 1 #현재 자기자본율의 100% 를 사용하겠다는 뜻 , 50% 라면 0.5로 수정 필요
                    order_size = math.floor(avail_size * math.floor(float(last_price))*0.99) #order size 는 USD 기준으로 표기해야하니 avail_size(BTC) * last price USD/BTC 적용, 0.99% 는 수수료를 위해 1% 마진
                    order.order("Sell",order_size) #가용 자산 만큼 풀 매수 이 때 위에서 버림으로 order_size 를 int 형으로 만들어줌
                    break
            else:
                pass
    else:
        pass