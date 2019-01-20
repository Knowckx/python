from bookut import bookdiff,mean,utlist
from .signset import *
# from signal import *


class Core:
    def __init__(self,maxGap = 1):
        self.High = -1
        self.Low = -1
        self.MaxGap = maxGap
        self.SignH = Signal(2)
        self.SignL = Signal(-2)
        self.histyL = [] # 记录历史上的决策
        pass

    def Refresh(self,bookL,i):
        self.NbookL = bookL
        self.Nprc = mean.GetPredictP(bookL[:])
        self.dif = difToSignal(bookL[:])
        self.lmt = utlist.AvgLotL(bookL[:])*1.5
        self.i = i

    def PutNew(self, bookL,i=-1):
        self.Refresh(bookL,i)
        if self.High == -1: #first
            self.High = self.Nprc
            self.Low = self.Nprc
            return 
        print('prc %s  his: %s %s'%(self.Nprc,self.Low,self.High))
        if self.Low <= self.Nprc <= self.High:  #区间值
            self.DealMid()
            return
        elif self.Nprc < self.Low:  # 下破
            self.OpenLow()
            return 
        elif self.Nprc > self.High:
            self.OpenHigh()
            return

    # 区间值操作
    def DealMid(self): 
        print("Mid")
        self.UpdateH()
        self.UpdateL()

    def OpenLow(self):
        print("new Lower")
        self.SignL.Reset(self.i,self.Nprc,self.lmt)  # 低集重新计数
        self.Low = self.Nprc # 低价 更新
        if self.CheckGap(): # 有时需要更新高价
            self.High = self.Low + self.MaxGap
        self.UpdateH() # 不确定SighH要不要更新

    def OpenHigh(self):
        print("new Higher")
        self.SignH.Reset(self.i,self.Nprc,self.lmt)  # 重置高集
        self.High = self.Nprc
        if self.CheckGap():
            self.Low = self.High - self.MaxGap
        self.UpdateL()


 
    # 低值，要不要buy?
    def UpdateL(self):
        if isZero(self.dif):
            return
        ok,ss = self.SignL.Update(self.dif)
        if ss == '500': #Signal is Closed
            return
        print("try update Sign low")
        print("Sign Low:",ok,ss)
        if ok:
            self.addHis(TupleToList(self.SignL.GetHisEx()))
            self.SignL.Close()
            self.OpenHigh()

    # 峰值，要不要sell?
    def UpdateH(self):
        if isZero(self.dif): # 过滤diff为0的盘面
            return
        ok,ss = self.SignH.Update(self.dif) # 判断..
        if ss == '500': #Signal is Closed
            return
        print("try update Sign High")
        print("Sign High:",ok,ss)
        if ok:  # 确定是个高点回落信号
            self.addHis(TupleToList(self.SignH.GetHisEx()))
            self.SignH.Close()
            self.OpenLow()

    def CheckGap(self):
        return (self.High - self.Low) > self.MaxGap


    def PrintStatus(self):
        print("high and low:",self.High,self.Low)
        print("Sign high and low:",self.SignH,self.SignL)

    def DumpHisty(self):
        print("DumpCoreHisty:")
        for his in self.histyL:
            print(his)
    
    def addHis(self,L):
        hisL = self.histyL
        if len(hisL) > 0:
            last = hisL[-1]
            dif = GetDifPst(last[1],L[1])
            last.append(dif)
        self.histyL.append(L)

# book - bookdif - [+-11]上的变动
def difToSignal(bookL):
    difL = bookdiff.Start(bookL[:])
    rst = [0,0]
    f = 0
    for dif in difL[:]:
        p,l = dif[0],dif[1]
        if abs(p) >11: #先确定系数
            cnt = abs(p) - 11
            f = 1/pow(2,cnt+1)
        else:
            f = 1
        vv = f*l #转换过来的数量
        if abs(vv) < 1 :
            continue
        if vv > 0: # 多
            rst[0] = rst[0] + vv
        else: # 空
            rst[1] = rst[1] + abs(vv)
    print('diff:%s ToSign:%s'%(difL[:],rst))
    return rst


# 两数差值的百分比
def GetDifPst(v1,v2):
    dif = (v2 - v1)/v1*100
    return round(dif,2)

def TupleToList(tu):
    rst = []
    for t in tu:
        rst.append(t)
    return rst


def isZero(dd):
    if dd[0]==0 and dd[1]==0:
        print("dd is %s.Pass"%dd)
        return True
    return False