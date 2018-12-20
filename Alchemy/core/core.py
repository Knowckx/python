
from bookut import bookdiff,mean


class Core:
    def __init__(self):
        self.High = -1
        self.Low = -1
        self.MaxGap = 1
        self.SignH = Signal()
        self.SignL = Signal()
        pass


    def PutNew(self, bookL):
        prc = mean.GetPredictP(bookL[:])

        if self.High == -1: #first
            self.High = prc
            self.Low = prc
            return 
        if self.Low < prc < self.High:  #区间值
            DealMid(bookL)
        elif prc < self.Low:  # 下破
            DealLow(prc)
            return 
        elif prc > self.High:
            DealHigh(prc)
            return


    def DealLow(self,prc):
        self.Low = prc
        self.SignL.Reset()
        if CheckGap:
            self.High = self.Low + self.MaxGap

    def DealHigh(self,prc):
        self.High = prc
        self.SignH.Reset()
        if CheckGap:
            self.Low = self.High - self.MaxGap

    # 区间值操作
    def DealMid(self,bookL): 
        bDif = bookdiff.Start(bookL[:])
        dd = difToSignal(bDif)
        self.SignH.Update(dd)
        self.SignL.Update(dd)
        self.SignH.IsAction()
        self.SignL.IsAction()
        pass



    
    # --- 小家伙们
    # Signal 判断信号集 Signal[多量,空量]
    def InitSignal(self):
        self.CloseSignH()
        self.CloseSignH()
        
    # Signal 判断信号集 Signal[多量,空量,是否开启]





    def CheckGap(self):
        return self.Gap > self.MaxGap

    def Gap(self):
        v = self.High - self.Low


 
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
        self.Signal = [0,0] 
        self.Open = False
    def IsOpen(self):
        return self.Open 


    def Update(self,dd):
        if !self.IsOpen():  #is close
            return False,"Closed"
        self.VV[0] = self.VV[0]+dd[0]
        self.VV[1] = self.VV[1]+dd[1]
        return self.IsAction()

    def IsAction(self):
        bid = self.VV[0]
        ask = self.VV[1]
        if (bid + ask) < 12 #数量够
            return  False,"Count not enough"
        if self.Flag > 0:
            
        if ask == 0:
            return True,"Count not enough"
            if bid >= self.Flag*ask
                reutrn True
        if self.Flag < 0:
            if ask >= self.Flag*bid*(-1)
                reutrn True
        return False
        
# 一次盘面结果转为 +-11上的变动
def difToSignal(difL):
    rst = [0,0]
    f = 0
    for dif in difL[:]:
        p,l = dif[0],dif[1]
        if abs(p) >=11: #先确定系数
            cnt = p - 11
            f = pow(2,cnt)
        else:
            f = 1.2
        vv = l*f #转换过来的数量
        if vv < 1 :
            continue
        if p > 0: # 多
            rst[0] = rst[0] + vv
        else: # 空
            rst[1] = rst[1] + vv
    return rst
            



