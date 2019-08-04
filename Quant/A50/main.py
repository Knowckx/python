import Quant.A50.data.csv as csv
import Quant.A50.SLG.dvg as dvg
import sys


def test():
    tarFile = '000925.XSHG_1d'
    df = csv.GetPDdata(tarFile)  # data prepare

    # print(df[-1:])  # test DF

    startData = "2013-12-27"
    idx = GetDateIndex(df,startData)
    while idx < df.index[-1]:
        dftest = df.loc[idx-200:idx]
        # print(dftest[-3:])
        dvg.Start(dftest)
        idx +=1



def GetDateIndex(df, date):
    timeL = df.time
    i = df.index[-1] #最后一个索引
    while i > 0: 
        if timeL.at[i] == date:
            return i
        i -= 1
    return 0


test()
