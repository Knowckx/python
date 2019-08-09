import Quant.A50.data.csv as csv
import Quant.A50.SLG.dvg as dvg
import datetime



def test():
    tarFile = '000925.XSHG_1d'
    df = csv.GetPDdata(tarFile)  # data prepare

    # print(df[-1:])  # test DF

    startData = "2013-12-27 00:00:00"
    idx = GetDateIndex(df,startData)
    while idx < df.index[-1]:
        dftest = df.loc[idx-200:idx]
        # print(dftest[-1:])
        dvg.Start(dftest)
        idx +=1


# 在df里找到对应的时间index
def GetDateIndex(df, date):
    timeL = df.time
    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    i = df.index[-1] #最后一个索引
    while i > 0: 
        strtime = timeL.at[i] #从csv读出来是字符串
        dftime = datetime.datetime.strptime(strtime, "%Y-%m-%d")
        if dftime <= date:
            return i
        i -= 1
    return 0


test()



