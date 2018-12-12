import libs.Win32Excel as ex
from bookut import bookdiff,extremum
from exut import booklist

sht =1

AskL1 = []
BidL1 = []

AskL2 = []
BidL2 = []

#盘口变化
def SetDiff():
    global sht,AskL1,BidL1,AskL2,BidL2
    sht = ex.InitExcelSht()
    booklist.sht = sht

    i = 1
    # i = 3145 #debug

    k = 0 #lastL
    while True:
        i = i + 1
        prc = sht.Cells(i, 2).Value
        print(i,prc)

        if prc == None or prc == "":
            break
        if prc == "Bid5":
            i = i + 1
            if len(AskL1)==0:
                k = i
                BidL1,AskL1 = booklist.GetBookEx(k,2)
                
            else:
                BidL2,AskL2 = booklist.GetBookEx(i,2)
                rstDiff = bookdiff.Start(AskL1,BidL1,AskL2,BidL2,Screen=0)
                sht.Cells(k, 14).Value = str(rstDiff)

                DiffL = bookdiff.ScreenRst(rstDiff[:])
                if len(DiffL) ==0:
                    DiffL = None
                else:
                    DiffL = str(DiffL)
                sht.Cells(k, 17).Value = DiffL
                k = i
                BidL1,AskL1 = BidL2,AskL2
SetDiff()



