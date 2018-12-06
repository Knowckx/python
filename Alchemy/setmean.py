import libs.Win32Excel as ex
from exut import booklist
from bookut import mean
sht =1

AskL1 = []
BidL1 = []


# 期望值
def setmean():
    global sht,AskL1,BidL1
    sht = ex.InitExcelSht()
    booklist.sht = sht
    i = 1
    while True:
        i = i + 1
        prc = sht.Cells(i, 2).Value
        print(i,prc)
        if prc == None or prc == "":
            break
        if prc == "BookList":
            i = i + 1
            BidL1,AskL1 = booklist.GetBookEx(i,2)
            rst = mean.GetMeanPrice(AskL1,BidL1)
            sht.Cells(i, 7).Value = rst

setmean()



