
# import debugEx

DiffL = []


# 基础 确定是diff 加入
def DifApd(difP,difLots):
    for dif in DiffL:
        if dif[0] == difP:
            dif[1] = dif[1]+difLots
            return
    DiffL.append([difP,difLots])

# 同价单位，比较量是否有变化
def DifSame(L1,L2,mode=1):
    if(L1[0] != L2[0]):
        print("Need Same Price",L1[0],L2[0])
        return
    if(L1[1] == L2[1]):
        return
    difPrice = L2[0] 
    difLots = (L2[1] - L1[1])*mode
    DifApd(difPrice,difLots)

# 同价对比
def DifSames(L1,L2,mode=1):
    for i in range(0,len(L2)):
        DifSame(L1[i],L2[i],mode)

def diffBidL(BidL1,BidL2):
    if BidL1[0][0] == BidL2[0][0]: #平盘
        DifSames(BidL1,BidL2)
    elif BidL1[0][0] < BidL2[0][0]: #buy,右移
        addbuyR(BidL1,BidL2)
    elif BidL1[0][0] > BidL2[0][0]: #sell,左移
        addbuyR(BidL2,BidL1,-1)

def diffAskL(AskL1,AskL2):
    if AskL1[0][0] == AskL2[0][0]: #平盘
        DifSames(AskL1,AskL2,-1)
    elif AskL1[0][0] < AskL2[0][0]: #卖盘,右移
        addbuyR(AskL2,AskL1)
    elif AskL1[0][0] > AskL2[0][0]: #卖盘,左移
        addbuyR(AskL1,AskL2,-1)



def addbuyR(BidL1,BidL2,mode=1):
    for i in range(0,5):
        if BidL2[i][0] != BidL1[0][0]:
            prc = BidL2[i][0]
            lots = BidL2[i][1]*mode
            DifApd(prc,lots)
            continue
        DifSames(BidL1,BidL2[i:],mode)
        break

def SortDiffL(ut):
    return ut[0]



def Replace(BidL,AskL):
    for i in range(0,5):
        BidL[i][0] = (i+1)*(-1) 
        AskL[i][0] = i+1


def Start(AskL1,BidL1,AskL2,BidL2):
    global DiffL
    Replace(BidL1,AskL1)
    Replace(BidL2,AskL2)
    DiffL = []
    diffBidL(BidL1,BidL2)
    diffAskL(AskL1,AskL2)
    DiffL.sort(key=SortDiffL)
    return DiffL

def GetLists():
    AskL1,BidL1,AskL2,BidL2 = debugEx.main()
    Start(AskL1,BidL1,AskL2,BidL2)
 


# GetLists()


                
                
