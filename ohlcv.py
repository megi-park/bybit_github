import bybit
import mkdntjr12_bybit1
import datetime as dt
import pandas as pd

def ohlcv():    
    client = bybit.bybit(test=False, api_key=mkdntjr12_bybit1.api_key, api_secret=mkdntjr12_bybit1.secret_key)
    time = client.Market.Market_orderbook(symbol="BTCUSD").result() #서버 시간을 가져오는 것
    now = time[0]["time_now"]
    now = dt.datetime.fromtimestamp(int(float(time[0]["time_now"])))

    #현재 ~ 1000분 사이의 데이터를 가져오는 것, [0] 열은 현재 오픈된 봉도 가져오기 때문에 제거해주는 함수가 필요함.
    min_1000ago = dt.datetime.timestamp(now - dt.timedelta(minutes=1000)) #현재로부터 1000분 전, 5분 봉 기준으로 한 번에 200개 밖에 못 뽑아서 1000 분 기준으로
    data = client.Kline.Kline_get(symbol="BTCUSD", interval="5", **{'from':min_1000ago}).result()
    ohlcv = data[0]["result"]
    ohlcv_pd = pd.DataFrame(ohlcv)
    df1000 = ohlcv_pd.sort_values(by="open_time" , ascending=False)

    #1000~2000분의 데이터를 가져오는 것
    min_2000ago = dt.datetime.timestamp(now - dt.timedelta(minutes=2000)) #현재로부터 2000분 전, 5분 봉 기준으로 한 번에 200개 밖에 못 뽑아서 2000 분 기준으로
    data2 = client.Kline.Kline_get(symbol="BTCUSD", interval="5", **{'from':min_2000ago}).result()
    ohlcv2 = data2[0]["result"]
    ohlcv2_pd = pd.DataFrame(ohlcv2)
    df2000 = ohlcv2_pd.sort_values(by="open_time" , ascending=False)

    #현재 ~ 2000분 전의 데이터로 머지 하는 것 머지 후에 보기 쉬운 형식으로 바꿔줌
    df_merge = pd.concat([df1000, df2000])
    df_merge["open_time"]  = pd.to_datetime(df_merge["open_time"], unit='s') #datetime --> 우리가 보기 쉬운 꼴로 만들어줌

    '''
    #현재 시간 값을 계산해서 첫행이 5분 표를 나타내면 삭제하려고 하였으나, 10min 으로 converting 시 첫 행은 어차피 계속 가변 값을 가지므로 해당 함수가 필요 없어짐
    print(df_merge["open_time"].iloc[0])
    print(type(df_merge["open_time"].iloc[0]))
    cur_time = df_merge["open_time"].iloc[0] #pandas 의 시간함수는 기존 python 과는 다른 함수를 가지고 있음
    print(cur_time)
    print(type(cur_time))
    cur_time = cur_time.to_pydatetime() #파이썬의 date time 형태로 바꿔줌
    print(cur_time)
    print(type(cur_time))
    cur_min = int(cur_time.minute)
    print(cur_min/5)
    print(type(cur_min))
    '''

    df_merge = df_merge.reset_index() #index 를 reset 처리하고 index 열을 추가하는 것이나, 열은 아래에서 삭제
    df_merge = df_merge.drop(["index","symbol","interval","turnover","volume"], axis=1) #index 는 필요없고, 심볼은 중복 값이니 필요 없고, interval 은 10분으로 바꾸고, turnover, volume 은 필요 없으니 삭제
    df_merge = df_merge.set_index("open_time")  #index 를 open time 으로 바꾸는 것

    #ohlcv data 를 10분 기준으로 바꿔줌
    df_merge10 = df_merge.resample('10min').agg({'open': 'first', 
                                    'high': 'max', 
                                    'low': 'min', 
                                    'close': 'last'})

    #기본적으로 open time 기준으로 오름차순이나,내림차순으로 바꿔줌
    # print(df_merge10)
    df_merge10 = df_merge10.sort_values(by="open_time" , ascending=False) #merge 한뒤 데이터를 open time 에 맞춰 내림차순 정렬함 , 처음 값은 제외해야 할 듯
    # print(df_merge)
    # print(df_merge10)
    df_merge10_del = df_merge10.iloc[1:] #첫행은 계속 open 이후로 잡히고 있기 때문에 삭제해주는 index 1 열부터 가져오도록 함
    df_merge10_del = df_merge10_del.sort_values(by="open_time" , ascending=True) #diff 함수 자체가 윗열을 빼게 되기 때문에 다시 오름차순 정렬 해줌
    # print(df_merge10_del.info())
    df_merge10_del = df_merge10_del.astype(float) #str 으로 되어있는 것을 float type 으로 변경하도록
    # print(df_merge10_del.info())


    # now_sec = dt.datetime.fromtimestamp(int(float(time[0]["time_now"])))
    # print(now)
    print("ohlcv out 완료, 완료 시간 : {0}".format(now))


    # df_merge.to_csv("5min_ohlcv.csv", index = True) #csv 파일로 만들어주 400rows 에 대한 파일로 , 경로를 지정하고 싶으면 따로 확인해보기
    # df_merge10.to_csv("10min_ohlcv.csv", index = True) #csv 파일로 만들어주 400rows 에 대한 파일로 , 경로를 지정하고 싶으면 따로 확인해보괴
    df_merge10_del.to_csv("10min_del_ohlcv.csv", index = True) #csv 파일로 만들어주 400rows 에 대한 파일로 , 경로를 지정하고 싶으면 따로 확인해보괴
    return df_merge10_del

# client = bybit.bybit(test=False, api_key=mkdntjr12_bybit1.api_key, api_secret=mkdntjr12_bybit1.secret_key)
# time = client.Market.Market_orderbook(symbol="BTCUSD").result()
# now = time[0]["time_now"]
# now_sec = dt.datetime.fromtimestamp(int(float(time[0]["time_now"])))
# print(now)

# ohlcv()