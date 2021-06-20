import ohlcv
import rsi
import mkdntjr12_bybit1
import bybit
import datetime as dt

# whie True:
#     #현재 기준 
#     df1 = ohlcv.ohlcv() #ohlcv data 를 가져와 df1 에 저장
#     df2 = rsi.rsi(df1,14)
#     df2 = df2.sort_values(by="open_time" , ascending=False)
#     cur_RSI = df2.iloc[0]["RSI"] #마지막 10분 봉 기준의 RSI 값을 저장
#     print("현재 RSI 값 : {0}".format(cur_RSI))

client = bybit.bybit(test=False, api_key=mkdntjr12_bybit1.api_key, api_secret=mkdntjr12_bybit1.secret_key) #mkdntjr12_bybit1.secret_key
info = client.Market.Market_symbolInfo(symbol="BTCUSD").result()[0] # 마켓에서 거래되는 모든 거래쌍에 대한 현재 정보를 가져오는 것 keys 에 info 를 넣고 for i 문을 통해 안에 뭐가 들어있는지 확인이 가능함

print(info["time_now"])
now = dt.datetime.fromtimestamp(int(float(info["time_now"])))
print(now)
# #현재 시간 값을 계산해서 첫행이 5분 표를 나타내면 삭제하려고 하였으나, 10min 으로 converting 시 첫 행은 어차피 계속 가변 값을 가지므로 해당 함수가 필요 없어짐
# print(df_merge["open_time"].iloc[0])
# print(type(df_merge["open_time"].iloc[0]))
# cur_time = df_merge["open_time"].iloc[0] #pandas 의 시간함수는 기존 python 과는 다른 함수를 가지고 있음
# print(cur_time)
# print(type(cur_time))
# cur_time = cur_time.to_pydatetime() #파이썬의 date time 형태로 바꿔줌
# print(cur_time)
# print(type(cur_time))
# cur_min = int(cur_time.minute)
# print(cur_min/5)
# print(type(cur_min))