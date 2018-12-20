# from libs import FileRW
import libs.Win32Excel as ex
from bookut import bookdiff,mean

p = 0 #最近的new tick
ntCnt = 0 #已经传入多少次tick了
flag = 0 #最近一次的判断
PL3 = [] #3数的数组



#back test in excel

AskL2 = []
BidL2 = []

sht =1


# 传入最近的Book盘
def Core(bookL):
    # global AskL1,BidL1,AskL2,BidL2
    # BidL,AskL = b[0],b[1]
    # BidL2,AskL2 = b[0],b[1]

    rstDiff = bookdiff.Start(bookL[:],Screen=0)
    # diff到手

    theP = mean.GetPredictP(bookL[:])
    # 期望值到手

    # 这个值是什么概念？
    # 新高？ 新低？

    sht.Cells(k, 14).Value = str(rstDiff)

    DiffL = bookdiff.ScreenRst(rstDiff[:])
    if len(DiffL) ==0:
        DiffL = None
    else:
        DiffL = str(DiffL)
    sht.Cells(k, 17).Value = DiffL


    rst = dealPL3()
    print('listP status：',PL3)
    return rst
    # for p in PL3:
    #     pass
