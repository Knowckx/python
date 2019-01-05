import libs.Win32Excel as ex


sht = 1
LoopIdx = 1

def SetCell(i,v,rst):
    global sht
    sht.Cells(i, v).Value = rst

def InitSht():
    global sht
    sht = ex.InitExcelSht()

def GetPAL(ss):
    rs = str(ss).partition(",")
    ut = []
    ut.append(float(rs[0]))
    ut.append(int(rs[2]))
    return ut

# 拿到某行的book
def GetBookEx(row,col):
    BidL = []
    AskL = []
    
    for i in range(5,0,-1):
        vv = sht.Cells(row, col+i-1).Value
        vv = GetPAL(vv)
        BidL.append(vv)

    for i in range(0,5,1):
        vv = sht.Cells(row, col+i+6).Value
        vv = GetPAL(vv)
        AskL.append(vv)
    
    book = []
    book.append(BidL)
    book.append(AskL)
    return book


def BookNext():
    global LoopIdx
    book = []
    LoopIdx = LoopIdx - 1
    while True:
        LoopIdx = LoopIdx + 1
        prc = sht.Cells(LoopIdx, 2).Value
        if prc == None or prc == "":
            return book,LoopIdx
        if prc == "Bid5":
            LoopIdx = LoopIdx + 1
            book = GetBookEx(LoopIdx,2)
            return book,LoopIdx
        