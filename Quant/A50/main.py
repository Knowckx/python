
import pandas as pd


def GetPDdata():
    df1d=pd.read_csv('Quant/A50/csv/399925_1d.csv',index_col=0)
    return df1d

# 入口
def Start():
    df1d = GetPDdata() # data prepare
    print(df1d[-5:])


Start()