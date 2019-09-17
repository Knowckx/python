import pandas as pd


# 行情数据
def GetPDdata(filename):
    logPath = 'Quant/A50/csv/' + filename + '.csv'
    df1d=pd.read_csv(logPath,index_col=0)
    df1d['repv']= (df1d['close']+df1d['open']) /2
    return df1d


def GetPDExcel(filename,sheetname):
    logPath = 'Quant/A50/csv/' + filename + '.xlsx'
    df=pd.read_excel(logPath,sheet_name=sheetname)
    return df
