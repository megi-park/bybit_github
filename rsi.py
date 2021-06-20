import bybit
import ohlcv
import pandas as pd
import numpy as np

def rsi(data: pd.DataFrame,period):
    df1 = data
    # print(df1.info())
    # ohlcv.ohlcv() #인풋으로 데이터를 받음
    # df1 = pd.read_csv("10min_del_ohlcv.csv") #인풋으로 데이터를 받음
    # period = 14 #인풋으로 period 를 받음

    delta = df1["close"].diff(1)
    # delta = delta[1:] #지워버리면 열의 갯수가 맞지 않음

    up = delta.copy()
    up[up < 0 ] = 0
    AU = pd.DataFrame.ewm(up, alpha=1/period).mean()

    down = delta.copy()
    down[down > 0 ] = 0
    down *= -1
    AD = pd.DataFrame.ewm(down, alpha=1/period).mean()

    df1["up"] = up
    df1["down"] = down
    RSI = np.where(AU == 0, 0, np.where(AD == 0, 100, round(100 - (100 / (1 + AU / AD)),2) ))

    df1["AU"] = AU
    df1["AD"] = AD
    df1["RSI"] = RSI
    df1.to_csv("RSI.csv",index = True)
    
    # print(df1)
    return df1