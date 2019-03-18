#关于macd的计算方式

import pandas as pd
import numpy as np
import datetime
import time

#获取数据
df=pd.read_csv('Quant/talib/macd/df_close.csv',index_col=0)

# 这个手动算法，计算一次MACD就需要0.5s....

def get_EMA(df,N):
    for i in range(len(df)):
        if i==0:
            df.loc[i,'ema']=df['close'][i]
        if i>0:
            df.loc[i,'ema']=(2*df['close'][i]+(N-1)*df['ema'][i-1])/(N+1)
    ema=list(df['ema'])
    return ema

def get_MACD(df,short=12,long=26,M=9):
    a=get_EMA(df,short)
    b=get_EMA(df,long)
    df['diff']=pd.Series(a)-pd.Series(b)
    for i in range(len(df)):
        if i==0:
            df.loc[i,'dea']=df['diff'][i]
        if i>0:
            df.loc[i,'dea']=(2*df['diff'][i]+(M-1)*df['dea'][i-1])/(M+1)
    df['macd']=2*(df['diff']-df['dea'])
    return df

start = time.time()
get_MACD(df,12,26,9)
end = time.time()
print(df)
print("cost time:"+ str(end -start))


