import Quant.A50.data.csv as csv
import Quant.A50.SLG.dvg as dvg
import Quant.A50.SLG.BackTest as bt
import datetime


def StartBTest():
    srcFile = '000925.XSHG_5m' # 不用后缀名
    shName = '5m' # 同grade
    bTest = bt.BackTest(shName)
    df = csv.GetPDdata(srcFile)  # data prepare
    # print(df[-2:])
    bTest.StartWith(df,shName) 



def test():
    StartBTest()  #回测路线
    return 
    # tarFile = '000925.XSHG_5m'
    
    srcFile = '000925.XSHG_5m'
    df = csv.GetPDdata(srcFile)  # data prepare

    startData = "2019-09-05 14:20:00"
    # startData = "2017-09-29"

    dvg.Init('5m')

    idx = GetDateIndex(df,startData)
    while idx < df.index[-1]:
        dftest = df.loc[idx-200:idx]
        # print(dftest[-3:])
        rst = dvg.Start(dftest)
        if (rst.F_hl !=0):
            # print(rst.String())
            rst.Print()
        idx +=1


# 在df里找到对应的时间index
def GetDateIndex(df, date):
    timeL = df.time
    FormatDate = "%Y-%m-%d %H:%M:%S"
    if len(date) == 10:
        FormatDate = "%Y-%m-%d"
    date = datetime.datetime.strptime(date, FormatDate)
    i = df.index[-1] #最后一个索引
    while i > 0: 
        strtime = timeL.at[i] #从csv读出来是字符串
        dftime = datetime.datetime.strptime(strtime, FormatDate)
        if dftime <= date:
            return i
        i -= 1
    return 0


test()



