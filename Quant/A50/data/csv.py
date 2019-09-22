import pandas as pd


# 行情数据
def GetPDdata(filename):
    logPath = 'Quant/A50/csv/' + filename + '.csv'
    df=pd.read_csv(logPath,index_col=0)
    # df['repv']= (df['close']+df['open']) /2
    # df.sort_index(axis=0,ascending=False,inplace = True)
    # df['borate']= round((df['bup']-df['blow']) / df['blow'] *100,4)
    return df


def GetPDExcel(filename,sheetname):
    logPath = 'Quant/A50/csv/' + filename + '.xlsx'
    df=pd.read_excel(logPath,sheet_name=sheetname)
    return df
