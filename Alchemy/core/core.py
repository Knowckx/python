from bookut import bookdiff,mean,utlist


class Core:
    def __init__(self,maxGap = 1):
        self.High = -1
        self.Low = -1
        self.MaxGap = maxGap
        self.SignH = Signal(2)
        self.SignL = Signal(-2)
        pass


    def PutNew(self, bookL,i=-1):
        self.NbookL = bookL
        self.Nprc = mean.GetPredictP(bookL[:])
        self.dif = difToSignal(bookL[:])
        self.lmt = utlist.AvgLotL(bookL[:])*1.5
        self.i = i
        # print(prc,self.dif)
        # return
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



    def OpenLow(self):
        print("new Lower")
        self.SignL.Reset(self.i,self.lmt,)  # 重置低集
        self.Low = self.Nprc # 低价 更新
        if self.CheckGap():
            self.High = self.Low + self.MaxGap
        self.UpdateH()

    def OpenHigh(self):
        print("new Higher")
        self.SignH.Reset(self.i,self.lmt)  # 重置高集
        self.High = self.Nprc
        if self.CheckGap():
            self.Low = self.High - self.MaxGap
        self.UpdateL()

    # 区间值操作
    def DealMid(self): 
        print("Mid")
        self.UpdateH()
        self.UpdateL()
 
    # 峰值，要不要buy?
    def UpdateL(self):
        if isZero(self.dif):
            return
        ok,ss = self.SignL.Update(self.dif)
        if ss == '500': #Signal is Closed
            return
        print("try update Sign low")
        print("Sign Low:",ok,ss)
        if ok:
            self.SignL.Close()
            self.OpenHigh()

    # 峰值，要不要sell?
    def UpdateH(self):
        if isZero(self.dif):
            return
        ok,ss = self.SignH.Update(self.dif)
        if ss == '500': #Signal is Closed
            return
        print("try update Sign High")
        print("Sign High:",ok,ss)
        if ok:
            self.SignH.Close()
            self.OpenLow()

    def CheckGap(self):
        return self.Gap() > self.MaxGap

    def Gap(self):
        v = self.High - self.Low
        return v

    def PrintStatus(self):
        print("high and low:",self.High,self.Low)
        print("Sign high and low:",self.SignH,self.SignL)

 
# Class Signal 信号判断集
class Signal:
    def __init__(self,flag=2):
        self.Close()
        self.Flag = flag

    def Reset(self,i=-1,maxLimit=15):
        self.VV = [0,0] 
        self.Open = True
        self.CountLimit = maxLimit
        self.i = i
    def Close(self):
        self.VV = [0,0] 
        self.Open = False
    def IsOpen(self):
        return self.Open 

    def PrintNow(self):
        print("SignalStatus isopen:%s VV:%s"%(self.Open,self.VV))

    def Update(self,dd):
        if not self.IsOpen():  #is close
            return False,"500"
        self.PrintNow()
        self.VV[0] = self.VV[0]+dd[0]
        self.VV[1] = self.VV[1]+dd[1]
        self.PrintNow()
        ok,detail = self.IsAction()
        return ok,detail

    def IsAction(self):
        bid = self.VV[0]
        ask = self.VV[1]
        big = 0
        small = 0
        if (bid + ask) < self.CountLimit:  #self.CountLimit
            return  False,"Total Count not enough"
        if self.Flag > 0:  # 2是高位，big = ask
            if ask >= abs(self.Flag)*bid:
                return True,"Top! Sell!"
        if self.Flag < 0:
            if bid >= abs(self.Flag)*ask:
                return True,"low! buy!"
        return False,"Not Ready"
        
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




def isZero(dd):
    if dd[0]==0 and dd[1]==0:
        print("dd is %s.Pass"%dd)
        return True
    return False