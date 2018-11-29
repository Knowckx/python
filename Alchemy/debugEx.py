import libs.Win32Excel as ex
import bookdiff
sht =1

AskL1 = []
BidL1 = []

AskL2 = []
BidL2 = []

def loopforDiv():
    i = 0
    while True:
        i = i + 1
        print(i)
        prc = sht.Cells(i, 4).Value
        print(prc)
        if prc == None or prc == "":
            break

        if str(prc).find("[") > -1 or prc == "BookList":
            sht.Cells(i, 10).Value = prc
            sht.Cells(i, 4).Value = None
            print(prc)
        print(i, prc)
    return


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
    ut.append(float(rs[2]))
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



def main():
    global sht,AskL1,BidL1,AskL2,BidL2
    sht = ex.InitExcelSht()

    i = 1
    while True:
        i = i + 1
        prc = sht.Cells(i, 2).Value
        print(i,prc)

        if i >= 109:
            print(i,prc)


        if prc == None or prc == "" or i >= 510:
            break
        if prc == "BookList":
            i = i + 1
            if len(AskL1)==0:
                BidL1,AskL1 = GetBookEx(i,2)
            elif len(AskL2)==0:
                BidL2,AskL2 = GetBookEx(i,2)
            else:
                BidL1,AskL1 = BidL2,AskL2
                BidL2,AskL2 = GetBookEx(i,2)
                rstDiff = bookdiff.Start(AskL1,BidL1,AskL2,BidL2)
                sht.Cells(i, 14).Value = str(rstDiff)

main()
