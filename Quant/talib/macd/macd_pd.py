#关于macd的计算方式

import pandas as pd
import numpy as np
import datetime
import time

# #获取数据
df=pd.read_csv('Quant/talib/macd/df_close.csv',index_col=0)

#很棒。0.01秒计算完成
def get_MACD(df,short=12,long=26,mid=9):
    df["sema"] = df["close"].ewm(span=short).mean()
    df["lema"] = df["close"].ewm(span=long).mean()
    df['diff']=pd.Series(df["sema"])-pd.Series(df["lema"])

    df['dea']=pd.Series(df['diff']).ewm(span=mid).mean()
    df['macd']=2*(df['diff']-df['dea'])
    return df

def get_MACD_old(df,short=12,long=26,mid=9):
    df["sema"] = pd.ewma(df["close"],span=short1)
    df["lema"] = pd.ewma(df["close"],span=long1) 
    df['diff'] = pd.Series(df["sema"])-pd.Series(df["lema"])
    df["dea"] = pd.ewma(df["diff"],span=mid)
    df['macd']=2*(df['diff']-df['dea'])

start = time.time()
get_MACD(df)
end = time.time()
print(df)
print("cost time:"+ str(end -start))




