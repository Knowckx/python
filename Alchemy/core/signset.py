# Class Signal 信号判断集
class Signal:
    def __init__(self,flag=2):
        self.Close()
        self.Flag = flag

    def Reset(self,His=-1,HisP = -1,maxLimit=15):
        self.VV = [0,0] 
        self.Open = True
        self.CountLimit = maxLimit
        self.Cnt = 0 # 目前记录的次数
        self.SetHisEx(His,HisP)

    def SetHisEx(self,His,HisP):
        self.His = His    #极点位置
        self.HisP = HisP  #极点价格

    def GetHisEx(self):
        return self.His,self.HisP 

    def Close(self):
        self.VV = [0,0] 
        self.Open = False
    def IsOpen(self):
        return self.Open 

    def PrintNow(self):
        print("SignalStatus isopen:%s VV:%s"%(self.Open,self.VV))
    
    def Add(self,dd):
        self.VV[0] = self.VV[0]+dd[0]
        self.VV[1] = self.VV[1]+dd[1]
        self.Cnt = self.Cnt + 1
    
    def Update(self,dd):
        if not self.IsOpen():  #is close
            return False,"500"
        self.PrintNow()
        self.Add(dd)
        self.PrintNow()
        return self.IsAction()

    def IsAction(self):
        if self.Cnt <= 3:
            return  False,"Put Count not enough"
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





        



  