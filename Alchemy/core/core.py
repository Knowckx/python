from bookut import bookdiff,mean


class Core:
    def __init__(self,maxGap = 1):
        self.High = -1
        self.Low = -1
        self.MaxGap = maxGap
        self.SignH = Signal()
        self.SignL = Signal()
        pass


    def PutNew(self, bookL):
        prc = mean.GetPredictP(bookL[:])
        dd = difToSignal(bookL[:])
        print(prc,dd)
        if self.High == -1: #first
            self.High = prc
            self.Low = prc
            return 
        if self.Low < prc < self.High:  #区间值
            self.DealMid(dd,prc)
            return
        elif prc < self.Low:  # 下破
            self.DealLow(dd,prc)
            return 
        elif prc > self.High:
            self.DealHigh(dd,prc)
            return


    def DealLow(self,dd,prc):
        print("new Lower")
        self.Low = prc
        self.SignL.Reset()
        if self.CheckGap():
            self.High = self.Low + self.MaxGap
        self.UpdateH(dd,prc)

    def DealHigh(self,dd,prc):
        print("new Higher")
        self.High = prc
        self.SignH.Reset()
        if self.CheckGap():
            self.Low = self.High - self.MaxGap
        self.UpdateL(dd,prc)

    # 区间值操作
    def DealMid(self,dd,prc): 
        self.UpdateH(dd,prc)
        self.UpdateL(dd,prc)
 

    def UpdateL(self,dd,prc):
        ok,ss = self.SignL.Update(dd)
        print("Sign Low:",ok,ss)
        if ok:
            self.SignL.Close()
            self.SignH.Reset()
            self.High = prc

    def UpdateH(self,dd,prc):
        ok,ss = self.SignH.Update(dd)
        print("Sign High:",ok,ss)
        if ok:
            self.SignH.Close()
            self.SignL.Reset()
            self.Low = prc

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
    def __init__(self):
        self.Init()
        pass

    def Init(self):
        self.Close()
        self.Flag = 2

    def Reset(self):
        self.VV = [0,0] 
        self.Open = True
    def Close(self):
        self.VV = [0,0] 
        self.Open = False
    def IsOpen(self):
        return self.Open 


    def Update(self,dd):
        print("Signal status",self.Open,self.VV)
        if not self.IsOpen():  #is close
            return False,"Signal is Closed"
        self.VV[0] = self.VV[0]+dd[0]
        self.VV[1] = self.VV[1]+dd[1]
        return self.IsAction()

    def IsAction(self):
        bid = self.VV[0]
        ask = self.VV[1]
        big = 0
        small = 0
        if (bid + ask) < 12:
            return  False,"Total Count not enough"
        if self.Flag > 0:
            big,small = bid,ask
        if self.Flag < 0:
            big,small = ask,bid
        if big >= abs(self.Flag)*ask:
            return True,"gogogo"
        return False,"Not Ready"
        
# book - bookdif - [+-11]上的变动
def difToSignal(bookL):
    difL = bookdiff.Start(bookL[:])
    rst = [0,0]
    f = 0
    for dif in difL[:]:
        p,l = dif[0],dif[1]
        if abs(p) >=11: #先确定系数
            cnt = abs(p) - 11
            f = 1/pow(2,cnt)
        else:
            f = 1.2
        vv = f*l #转换过来的数量
        if abs(vv) < 1 :
            continue
        if vv > 0: # 多
            rst[0] = rst[0] + vv
        else: # 空
            rst[1] = rst[1] + abs(vv)
    return rst




