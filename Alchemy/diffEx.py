import libs.Win32Excel as ex
import bookdiff,extremum
sht =1

AskL1 = []
BidL1 = []

AskL2 = []
BidL2 = []

# com操作excel

# 形态
# BidL [Bid1 B2 B3 B4 B5]
# AskL [Ask1 A2 A3 A4 A5]
# Core

# PAL Price and Lots
def GetPAL(ss):
    rs = str(ss).partition(",")
    ut = []
    ut.append(float(rs[0]))
    ut.append(int(rs[2]))
    return ut

def GetBookEx(row,col):
    BidL = []
    AskL = []
    Core = -1

    for i in range(5,0,-1):
        vv = sht.Cells(row, col+i-1).Value
        vv = GetPAL(vv)
        BidL.append(vv)

    for i in range(0,5,1):
        vv = sht.Cells(row, col+i+6).Value
        vv = GetPAL(vv)
        AskL.append(vv)
    return BidL,AskL


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



