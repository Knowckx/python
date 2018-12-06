sht = 1

def GetPAL(ss):
    rs = str(ss).partition(",")
    ut = []
    ut.append(float(rs[0]))
    ut.append(int(rs[2]))
    return ut

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
    return BidL,AskL

