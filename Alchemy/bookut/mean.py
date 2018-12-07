
# 根据盘面计算数据期望值

def GetMeanPrice(AskL,BidL):
    askP,askLots = getMidMeanFromList(AskL)
    bidP,bidLots = getMidMeanFromList(BidL)

    rPrs = (askP+bidP)/(askLots+bidLots)
    rst = round(rPrs, 5)
    return rst

def getMidMeanFromList(Li):
    TotalP = 0
    TotalLots = 0
    for i in range(0,3):
        if Li[i][1] == 0:
            continue
        theLots = 1/Li[i][1]
        TotalLots = TotalLots + theLots
        TotalP = TotalP + Li[i][0]*theLots
    return TotalP,TotalLots