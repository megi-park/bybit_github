import bybit
import time
import datetime
import mkdntjr12_bybit1
import pandas as pd
import balance as bl
import order
import ohlcv
import rsi

client = bybit.bybit(test=False, api_key=mkdntjr12_bybit1.api_key, api_secret=mkdntjr12_bybit1.secret_key)
info = client.Market.Market_symbolInfo(symbol="BTCUSD").result() # 마켓에서 거래되는 모든 거래쌍에 대한 현재 정보를 가져오는 것 keys 에 info 를 넣고 for i 문을 통해 안에 뭐가 들어있는지 확인이 가능함
#로그인 이후 간단한 정보 기입, 24시간 관련 정보 기입 필요
print("로그인")
# print("BTCUSD 이번 펀딩 rate : {0}%".format(100*float(info[0]["result"][0]["funding_rate"])))
# print("BTCUSD 다음 펀딩 rate : {0}%".format(100*float(info[0]["result"][0]["predicted_funding_rate"])))
print("BTCUSD 이번 펀딩 rate : {0}%".format(round(100*float(info[0]["result"][0]["funding_rate"]),4)))            #너무 복잡하니까 펀딩비 소수점으로 바꿔버리기
print("BTCUSD 다음 펀딩 rate : {0}%".format(round(100*float(info[0]["result"][0]["predicted_funding_rate"]),4)))  #너무 복잡하니까 펀딩비 소수점으로 바꿔버리기

#잔고 표시
print("현재 자산")
bl.balance("BTC") # 리턴 값은 [0] : equity , [1] : available_balance, [2] : wallet_balance, [3] : unrealised_pnl, [4] : realised_pnl
#현재 포지션 표시
print("현재 포지션")
bl.position("BTCUSD")  #포지션 진입 시간을 좀 더 간단하게 나타낼 수 있으면 좋을 듯 , 보유기간 잘못나오고 있음, - updated at 이라 펀딩비 받는 시간 그대로 업데이트 되는 듯 함

#ohlcv data 가져오기
df1 = ohlcv.ohlcv() #ohlcv data 를 가져와 df1 에 저장
df2 = rsi.rsi(df1,14)
df2 = df2.sort_values(by="open_time" , ascending=False)
cur_RSI = df2.iloc[0]["RSI"] #마지막 10분 봉 기준의 RSI 값을 저장
print("현재 RSI 값 : {0}".format(cur_RSI))
# print(info[0]["result"][0]["last_price"]) #현재의 마지막 거래 가격

while True:
    time.sleep(5)
    #ohlcv data 가져오기
    df1 = ohlcv.ohlcv() #ohlcv data 를 가져와 df1 에 저장
    df2 = rsi.rsi(df1,14)
    df2 = df2.sort_values(by="open_time" , ascending=False)
    cur_RSI = df2.iloc[0]["RSI"] #마지막 10분 봉 기준의 RSI 값을 저장
    cur_time = df2.index[0]
    cur_side = bl.position("BTCUSD")[0]
    cur_size = bl.position("BTCUSD")[1]
    print("현재 RSI 값 : {0}".format(cur_RSI))
    if cur_RSI <=21:
        while True:
            time.sleep(5)
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
                    pass
                elif cur_side == "Sell": #포지션 변경 , 자기자본율 100%
                    cur_size = cur_size * 1 #자기 자본율 100% - 50일 경우 0.5 로 수정 필요
                    order.order("Buy",cur_size)
                    avail_size = bl.balance("BTC")[1] #매도 이후 현재 가용자산
                    order.order("Buy",avail_size) #가용 자산 만큼 풀 매수
                    break
                else:
                    avail_size = bl.balance("BTC")[1] #매도 이후 현재 가용자산
                    order.order("Buy",avail_size) #가용 자산 만큼 풀 매수
                    break
            else:
                pass
    elif cur_RSI >= 70:
        while True:
            time.sleep(5)
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
                    pass
                elif cur_side == "Buy": #포지션 변경 , 자기자본율 100%
                    cur_size = cur_size * 1 #자기 자본율 100% - 50일 경우 0.5 로 수정 필요
                    order.order("Sell",cur_size)
                    avail_size = bl.balance("BTC")[1] #매도 이후 현재 가용자산
                    order.order("Sell",avail_size) #가용 자산 만큼 풀 매수
                    break
                else:
                    avail_size = bl.balance("BTC")[1] #매도 이후 현재 가용자산
                    order.order("Sell",avail_size) #가용 자산 만큼 풀 매수
                    break
            else:
                pass
    else:
        pass