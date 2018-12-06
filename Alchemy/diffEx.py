import libs.Win32Excel as ex
import bookdiff,extremum
sht =1

AskL1 = []
BidL1 = []

AskL2 = []
BidL2 = []

#盘口变化
def main():
    global sht,AskL1,BidL1,AskL2,BidL2
    sht = ex.InitExcelSht()

    i = 1
    # i = 3145

    k = 0 #lastL
    while True:
        i = i + 1
        prc = sht.Cells(i, 2).Value
        print(i,prc)

        if prc == None or prc == "":
            break
        if prc == "BookList":
            i = i + 1
            if len(AskL1)==0:
                BidL1,AskL1 = GetBookEx(i,2)
                k = i
            else:
                BidL2,AskL2 = GetBookEx(i,2)
                rstDiff = bookdiff.Start(AskL1,BidL1,AskL2,BidL2)
                sht.Cells(k, 17).Value = str(rstDiff)
                k = i
                BidL1,AskL1 = BidL2,AskL2


main()



