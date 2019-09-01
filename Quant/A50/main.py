import Quant.A50.data.csv as csv
import Quant.A50.SLG.dvg as dvg
import Quant.A50.SLG.BackTest as bt
import datetime


def StartBTest():
    srcFile = '000925.XSHG_1d'
    shName = '1d'
    bTest = bt.BackTest(shName)
    df = csv.GetPDdata(srcFile)  # data prepare
    # df = UserDtdPrice(df)
    bTest.StartWith(df) 

# def UserDtdPrice(df):
#     df.clo  

def test():
    StartBTest()  #回测
    return
    # tarFile = '000925.XSHG_5m'
    srcFile = '000925.XSHG_1d'

    # startData = "2013-12-27 00:00:00"
    # startData = "2019-02-26 00:00:00"
    startData = "2018-01-01 00:00:00"

    df = csv.GetPDdata(srcFile)  # data prepare

    idx = GetDateIndex(df,startData)
    while idx < df.index[-1]:
        dftest = df.loc[idx-200:idx]
        # print(dftest[-1:])
        rst = dvg.Start(dftest,"1d")
        if (rst.F_hl !=0):
            # print(rst.String())
            rst.Print()
        idx +=1

FormatDateTime1 = "%Y-%m-%d"
FormatDateTime2 = "%Y-%m-%d %H:%M:%S"


# 在df里找到对应的时间index
def GetDateIndex(df, date):
    timeL = df.time
    date = datetime.datetime.strptime(date, FormatDateTime2)
    i = df.index[-1] #最后一个索引
    while i > 0: 
        strtime = timeL.at[i] #从csv读出来是字符串
        dftime = datetime.datetime.strptime(strtime, FormatDateTime1)
        if dftime <= date:
            return i
        i -= 1
    return 0


test()



