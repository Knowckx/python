import pandas as pd

def GetPDdata(filename):
    logPath = 'Quant/A50/csv/' + filename + '.csv'
    df1d=pd.read_csv(logPath,index_col=0)
    return df1d


def GetPDExcel(filename,sheetname):
    logPath = 'Quant/A50/csv/' + filename + '.xlsx'
    df1d=pd.read_excel(logPath,sheet_name=sheetname)
    return df1d
