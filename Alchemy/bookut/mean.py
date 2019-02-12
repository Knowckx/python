from Alchemy.bookut import utlist
import math


# mean 4.0 评估算法

# 向外暴露
def GetPredictP(book):
    
    return SSDD(book)





def SSDD(book):
    BidL,AskL = book[0],book[1]
    avgLots = utlist.AvgLotL(book[:]) #平均量是多少
    print("avgLots is ",avgLots)

    repBidL = GetRepFromLL(BidL,avgLots) #代表价格
    print("repBid is ",repBidL)
    repAskL = GetRepFromLL(AskL,avgLots)
    print("repAsk is ",repAskL)

    rst = getPredickt(repBidL,repAskL)
    print("mean is ",rst)
    return rst

# 取得代表值和代表量
def GetRepFromLL(LL,avgLots):
    repPrc = GetRepPrc(LL,avgLots) #代表价格
    repLots = GetRepLots(LL,repPrc)
    return [repPrc,repLots]

# 某个数组的“代表值”  represent
def GetRepPrc(LL,stdLots):
    sLL = GetSimpleList(LL,stdLots) # 抽样数组
    prc = GetCenterPrcFromList(sLL) # 重心值
    return prc

# 一个数组，给定抽样的量，返回结果集的数组
def GetSimpleList(LL,N):
    rst = []
    for i in range(0,len(LL)):
        if LL[i][1] >= N:  #这个位置能搞定了！
            rst.append([LL[i][0],N])
            break
        rst.append(LL[i])
        N = N - LL[i][1]
    return rst

# 从一个列表中，获得平均值(重心值)
def GetCenterPrcFromList(LL):
    total = 0
    count = 0
    for i in range(0,len(LL)):
        total = total + LL[i][0]*LL[i][1]
        count = count + LL[i][1]
    rst = total / count
    return rst

# 得到加权后的代表交易量
def GetRepLots(LL,RepPrc):
    flag = 1
    if LL[0][0] < LL[1][0]:
        flag = -1
    
    totalLots = 0
    for i in range(0,len(LL)):
        difPrc = (LL[i][0] - RepPrc)*flag # 插值多少
        vx = difPrc/RepPrc*100 # 坐标是多少
        factor = math.pow(2,vx) # 实际的权值
        theLots = LL[i][1]*factor # 本次加权的交易量
        totalLots = totalLots + theLots
        if flag == -1:
            print(difPrc,vx,factor,LL[i][1],theLots)
    return totalLots


# 最后 算反向重力值（盘口预测）
def getPredickt(bidL,askL):
    askP = askL[0]
    bidP = bidL[0]
    askLots = askL[1]
    bidLots = bidL[1]
    rPrs = (askP*bidLots+bidP*askLots)/(askLots+bidLots)
    return rPrs



