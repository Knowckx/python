from bookut import mean,utlist
import corefunc

# Class Signal 信号判断集
class Signal:
    def __init__(self,vtype,flag=2):
        self.Close()
        self.Type = vtype #类型 1 高点判断集 -1 低点判断集
        self.Flag = vtype*2 #破位信号比例
        self.Open = True #是否起效

    def Reset(self,bookL,HisI):
        self.HisI = HisI # 极点值的序号
        self.HisV = mean.GetPredictP(bookL[:])  #极点价格
        self.Limit = utlist.AvgLotL(bookL[:])*1.5 #破位信号总量

        self.VV = [0,0] #多空数量
        self.Cnt = 0 # 目前记录的次数
        self.Open = True #是否起效

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
    
    def Update(self,bookL,HisI):
        if not self.IsOpen():  #1.is closed
            return 501
        NewV = mean.GetPredictP(bookL[:])  #2.是否是极值的reset操作
        if (self.Type == 1 and NewV > self.HisV) or (self.Type == -1 and NewV < self.HisV):
            self.Reset(bookL,HisI)
            return 502

        diff = corefunc.difToSignal(bookL[:]) #本次的变动
        if isZero(diff): # 3.过滤diff为0的盘面
            return 503
        
        # 是值得更新的
        self.PrintNow()
        self.Add(newV)
        self.PrintNow()
        return self.IsAction()

    def IsAction(self):
        if self.Cnt <= 3: #次数不够
            return 301
        bid = self.VV[0]
        ask = self.VV[1]
        if (bid + ask) < self.Limit:  #bid + ask 总数不够
            return  302
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




        



  