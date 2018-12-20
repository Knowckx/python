
# 给出盘面值
def GetPredictP(book):
    book[0] = BidL
    book[1] = AskL
    total = 0
    factor = [70,16,8,4,2]
    for i in range(0,5):
        blots = BidL[i][1]
        alots = AskL[i][1]
        if blots == 0:
            blots =1
        if alots == 0:
            alots =1
        bidl = [BidL[0][0],blots] #固定在盘口价来计算
        askl = [AskL[0][0],alots]
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