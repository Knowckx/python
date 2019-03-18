import pandas as pd

import talib as ta


df=pd.read_csv('Quant\talib\macd\df_close.csv')
dw['macd'], dw['macdsignal'], dw['macdhist'] = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
dw[['close','macd','macdsignal','macdhist']].plot()
