

# 新 双维盘面值
def GetPredictP(book):
    BidL,AskL = book[0],book[1]
    
    prcBid,prcAsk = BidL[0][0],AskL[0][0]   #目前的两边价格
    rstPrc = (prcBid + prcAsk)/2
    
    v1 = GetFacVol(BidL)
    v2 = GetFacVol(AskL)

    rstVV = round(v1 - v2,2)

    nM = mean(rstPrc,rstVV)
    return nM

# 新 拿List的估计量
def GetFacVol(li):
    factor = [70,16,8,4,2]
    total = 0
    for i in range(0,5):
        total = total + li[i][1]*factor[i]/100
    return total

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

# Class Mean 盘面评估
class mean:
    def __init__(self,prc,lots):
        self.prc = prc  #评估价格
        self.lots = lots #评估量

    def __gt__(self, meanV):
        if self.prc == meanV.prc :
            return self.lots > meanV.lots
        return self.prc > meanV.prc

    def __ge__(self, meanV):
        return self.__gt__(meanV) or self.__eq__(meanV)

    def __lt__(self, meanV):
        if self.prc == meanV.prc :
            return self.lots < meanV.lots
        return self.prc < meanV.prc

    def __le__(self, meanV):
        return self.__lt__(meanV) or self.__eq__(meanV)

    def __eq__(self, meanV):
        if self.prc == meanV.prc and self.lots == meanV.lots:
            return True
        return False



    def __add__(self, meanV):
        return self.prc + meanV.prc 

    def __sub__(self, meanV):
        return self.prc - meanV.prc 

    def __str__(self):
        return self.String()

    def String(self):
        # ss = '%.4f,%.3f' % (self.prc,self.lots)
        prc =round(self.prc,5)
        lots =round(self.lots,5)
        ss = '%s(%s)' % (prc,lots)
        return ss


# a1 = mean(5,10)
# a2 = mean(5,11)
# a1 = [a1,5]
# print('%s at %d' % (a1[0],a1[1]))
