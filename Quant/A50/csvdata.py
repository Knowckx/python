
import pandas as pd


def GetPDdata():
    df1m=pd.read_csv('Quant/A50/csv/1m.csv',index_col=0)
    df5m=pd.read_csv('Quant/A50/csv/5m.csv',index_col=0)
    return df1m,df5m


def Start():
    df1m,df5m = GetPDdata()
    print(df1m[-5:])


# Start()