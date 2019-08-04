import pandas as pd

def GetPDdata(filename):
    logPath = 'Quant/A50/csv/' + filename + '.csv'
    df1d=pd.read_csv(logPath,index_col=0)
    return df1d