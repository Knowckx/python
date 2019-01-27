from bookut import mean,utlist
from . import corefunc

# Class Signal 信号判断集
class Signal:
    def __init__(self,vtype,flag=2):
        self.Close()
        self.Type = vtype #类型 1 高点判断集 -1 低点判断集
        self.Flag = vtype*2 #破位信号比例
        self.Open = False #是否起效  默认false

    def Reset(self,book):
        self.HisI = book.HisI  #极点值的序号
        self.HisV = book.NewV  #极点价格
        self.Limit = book.GetAvgLot()*1 #破位信号总量

        self.VV = [0,0] #多空数量
        self.Cnt = 0 # 目前记录的次数
        self.Open = True #是否起效

        print("reset in I:%d Prc:%s AvgLot:%f"%(book.HisI,book.NewV,self.Limit))
    # def Sync(self,dif,newV):
    #     self.Dif = dif
    #     self.NewV = newV

    #返回相对历史极值
    def GetHisEx(self):
        return self.HisI,self.HisV 

    def Close(self):
        self.Open = False
    def IsOpen(self):
        return self.Open 

    def PrintNow(self):
        print("SignalStatus isopen:%s VV:%s"%(self.Open,self.VV))
    
    def Add(self,dd):
        self.VV[0] = self.VV[0]+dd[0]
        self.VV[1] = self.VV[1]+dd[1]
        self.Cnt = self.Cnt + 1
    
    def Update(self,book):
        if not self.IsOpen():  #1.is closed
            return 501
        NewV = book.NewV
        if (self.Type == 1 and NewV >= self.HisV) or (self.Type == -1 and NewV <= self.HisV):
            self.Reset(book)
            return 502

        if book.DifL == None: # 3.过滤diff为0的盘面
            return 503
        
        # 是值得更新的
        self.Add(book.DifL)
        print("Signal Updated:  VV %s"%(self.VV))
        return self.IsAction()

    def IsAction(self):
        if self.Cnt <= 3: #次数不够
            return 301
        bid = self.VV[0]
        ask = self.VV[1]
        if (bid + ask) < self.Limit:  #bid + ask 总数不够
            return  302
        if bid < 1 or ask < 1:  #反向必须有一手
            return  303
        big = 0
        small = 0
        f = 1/(abs(self.Flag) + 1)
        if self.Flag > 0:  # 2 高位
            if (ask - bid) >= self.Limit*f:
                return 1 #卖
        if self.Flag < 0:
            if (bid - ask) >= self.Limit*f:
                return -1 #买
        return 300 #就是还没满足条件

#判断标准1
        # if self.Flag > 0:  # 2 高位
        #     if ask >= abs(self.Flag)*bid:
        #         return True,"Top! Sell!"
        # if self.Flag < 0:
        #     if bid >= abs(self.Flag)*ask:
        #         return True,"low! buy!"




        



  