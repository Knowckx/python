
# mean 3.0 评估算法

# 向外暴露
def GetPredictP(book):
    BidL,AskL = book[0],book[1]
    
    # prcBid,prcAsk = BidL[0][0],AskL[0][0]   #目前的两边价格
    # rstPrc = (prcBid + prcAsk)/2
    
    # v1 = GetFacVol(BidL)
    # v2 = GetFacVol(AskL)

    # rstVV = round(v1 - v2,2)

    # nM = mean(rstPrc,rstVV)
    return nM
def SSDD(BidL,AskL):
    stdLots = GetSimpleLots(BidL,AskL)  # 先决定抽样多少量
    prcBid = GetRepPrc(BidL,stdLots)
    prcAsk = GetRepPrc(AskL,stdLots)
    print("stdLots is ",stdLots) 



# 本次抽样的量为多少
def GetSimpleLots(BidL,AskL):
    BLots = BidL[0][1] + BidL[1][1]
    ALots = AskL[0][1] + AskL[1][1] #两个交易量
    stdLots = BLots
    if ALots < BLots:
        stdLots = ALots
    return stdLots

# 小综合，某个数组的“代表值”  represent
def GetRepPrc(LL,stdLots):
    sLL = GetSimpleList(LL,stdLots) # 抽样数组
    prc = GetCenterPrcFromList(sLL) # 重心值
    print("stdLots is ",stdLots)

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



-------------------
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


# 旧 给出盘面值
def GetPredictP1(book):
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


