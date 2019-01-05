
# 有间隙的情况下，算站位的虚拟值
def GetFixPrc(book):
    BidL,AskL = book[0],book[1]
    prcBid,prcAsk = BidL[0][0],AskL[0][0]   #目前的两边价格
    StrdGap = prcBid - BidL[1][0]
    if (prcAsk - prcBid) > StrdGap: #特殊情况
        mid = (prcBid + prcAsk)/2
        prcBid =  mid - StrdGap/2
        prcAsk =  mid + StrdGap/2
    return prcBid,prcAsk


# 给出盘面值
def GetPredictP(book):
    prcBid,prcAsk = GetFixPrc(book[:])
    BidL = book[0]
    AskL = book[1] 
    total = 0
    factor = [70,16,8,4,2]
    for i in range(0,5):
        blots = BidL[i][1]
        alots = AskL[i][1]
        if blots == 0:
            blots =1
        if alots == 0:
            alots =1
        bidl = [prcBid,blots] #固定在盘口价来计算
        askl = [prcAsk,alots]
        p = getPredickt(bidl,askl)
        # print(p,factor[i])
        total = total + p*factor[i]/100
    rst = round(total, 5)
    return rst



# 算预测
def getPredickt(bidL,askL):
    askP = askL[0]
    bidP = bidL[0]
    askLots = askL[1]
    bidLots = bidL[1]
    rPrs = (askP*bidLots+bidP*askLots)/(askLots+bidLots)
    return rPrs

def GetWeightedP(li):
    totalLots = 0
    desc = 2
    for i in range(0,len(li)):
        if i == 0:
            factor = 4*2
        elif i == 1:
            factor = 2
        factor = factor/desc #第一个是1，尾加是2
        theLots = li[i][1]
        # print(theLots,factor,theLots*factor)
        totalLots = totalLots + theLots*factor
    
    return totalLots


# 旧 算重心
def getMeanFromList(Li):
    index = 3
    TotalP = 0
    TotalLots = 0
    for i in range(0,index):
        if Li[i][1] == 0:
            continue
        theP = Li[i][0]
        theLots = Li[i][1]
        TotalP = TotalP + theP*theLots
        TotalLots = TotalLots + theLots
    MeanP = TotalP/TotalLots
    return MeanP,TotalLots