


DiffL = []


# 基础 确定是diff 加入
def DifApd(difP,difLots,check = False):
    if check:
        for dif in DiffL:
            if dif[0] == difP:
                dif[1] = dif[1]+difLots
                return
    DiffL.append([difP,difLots])

    
# 两个L对比，L头相同
#   4 5 6 |  7 8 9
# 3 4 5   |    8 9 10
def DifSames(L1,L2,gap=0,flag=-1):
    minL = len(L1)
    if len(L2) < minL:
        minL = len(L2)
    start = flag*(11+gap)
    for i in range(0,minL):
        if(L1[i][1] == L2[i][1]):
            continue
        difPrice = start+i*flag
        difLots = (L2[i][1] - L1[i][1])*(-1)*flag
        DifApd(difPrice,difLots)

def diffList(BidL1,AskL1,BidL2,AskL2):
    flag = -1
    if BidL1[0][0] == BidL2[0][0]: #平盘
        DifSames(BidL1,BidL2,flag = flag)
    elif BidL1[0][0] > BidL2[0][0]: #sell,左移
        addOutwardL(BidL1,BidL2,flag = flag)
    elif BidL1[0][0] < BidL2[0][0]: #buy,右移
        addInwardL(BidL1,BidL2,stad = AskL1[0][0],flag = flag)


    flag = 1
    if AskL1[0][0] == AskL2[0][0]: #平盘
        DifSames(AskL1,AskL2,flag = flag)
    elif AskL1[0][0] < AskL2[0][0]: #卖盘,右移
        addOutwardL(AskL1,AskL2,flag = flag)
    elif AskL1[0][0] > AskL2[0][0]: #卖盘,左移
        addInwardL(AskL1,AskL2,stad = BidL1[0][0],flag = flag)

# L2的头部多了几个数    L2新出现的6,7不能确定真实相对名
# 3 4 5   |    8 9 10
#   4 5 6 |  7 8 9 
def addInwardL(L1,L2,stad = 0,flag=-1):
    gap = getGap(L2,L1)
    DifSames(L1,L2[gap:],gap = 0,flag=flag)
    k = 0 
    for i in range(0,gap):
        cur = L2[gap-i-1]
        if (flag < 0 and cur[0] < stad) or (flag > 0 and cur[0] > stad):
            difPrice = (9-i)*flag
            lots = cur[1]*flag*(-1)
            DifApd(difPrice,lots)
            continue
        difPrice = (11+k)*flag*(-1)
        lots = cur[1]*flag*(-1)
        DifApd(difPrice,lots,check=True)
        k = k + 1 


# L1的头部多了几个数  L1在里，L2向外
#   4 5 6 |  7 8 9
# 3 4 5   |    8 9 10
# flag bid=-1 ask=1 
def addOutwardL(L1,L2,flag=-1):
    #第几个数才相等？
    gap = getGap(L1,L2)
    DifSames(L1[gap:],L2,gap=gap,flag=flag)
    #头部数的处理
    for i in range(0,gap):
        difPrice = (11+i)*flag
        lots = L1[i][1]*flag
        DifApd(difPrice,lots,check = True)

# L1的前位置多出数来 L1[2] = L2[0]
def getGap(L1,L2):
    #第几个数才相等？
    gap = 0
    for i in range(0,len(L1)):
        if L1[i][0] == L2[0][0]: #以L1头部为标准
            gap = i
            break
    return gap


def SortDiffL(ut):
    return ut[0]


# 要不要对结果进行筛选
def ScreenRst(DiffL):
    limit = 5
    for dif in DiffL[:]:
        if  (-11 <=dif[0] <= 11):
            if -5 < dif[1] < 5:
                DiffL.remove(dif)
        elif (dif[0] == -12 or dif[0] == 12):
            if -10 < dif[1] < 10:
                DiffL.remove(dif)
        elif (dif[0] == -13 or dif[0] == 13):
            if -20 < dif[1] < 20:
                DiffL.remove(dif)
        elif (dif[0] < -13 or dif[0] > 13):
            if -40 < dif[1] < 40:
                DiffL.remove(dif)
    return DiffL

def Start(AskL1,BidL1,AskL2,BidL2,Screen = 1):
    global DiffL
    # Replace(BidL1,AskL1)
    # Replace(BidL2,AskL2)
    DiffL = []
    diffList(BidL1,AskL1,BidL2,AskL2)
    DiffL.sort(key=SortDiffL)
    if Screen == 1:
        DiffL = ScreenRst(DiffL)
    return DiffL

def GetLists():
    AskL1,BidL1,AskL2,BidL2 = debugEx.main()
    Start(AskL1,BidL1,AskL2,BidL2)
 


# GetLists()


                
                
