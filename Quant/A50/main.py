import Quant.A50.data.csv as csv
import Quant.A50.SLG.dvg as dvg
import datetime



def test():
    tarFile = '000925.XSHG_5m'
    df = csv.GetPDdata(tarFile)  # data prepare

    # print(df[-1:])  # test DF

    # startData = "2013-12-27 00:00:00"
    startData = "2019-08-02 15:00:00"
    # startData = "2019-08-09 14:50:00"


    

    idx = GetDateIndex(df,startData)
    while idx < df.index[-1]:
        dftest = df.loc[idx-200:idx]
        # print(dftest[-1:])
        dvg.Start(dftest,"5m")
        idx +=1

FormatDateTime = "%Y-%m-%d %H:%M:%S"

# 在df里找到对应的时间index
def GetDateIndex(df, date):
    timeL = df.time
    date = datetime.datetime.strptime(date, FormatDateTime)
    i = df.index[-1] #最后一个索引
    while i > 0: 
        strtime = timeL.at[i] #从csv读出来是字符串
        dftime = datetime.datetime.strptime(strtime, FormatDateTime)
        if dftime <= date:
            return i
        i -= 1
    return 0


test()



