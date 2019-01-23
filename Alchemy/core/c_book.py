from bookut import mean,utlist
from . import corefunc

# Class Signal 信号判断集
class CBook:
    def __init__(self,bookL,hisI):
        self.BookL =  bookL #盘面
        self.HisI = hisI #excel的位置
        self.Init()

    def Init(self):
        bookL =self.BookL
        self.DifL = corefunc.difToSignal(bookL[:]) #统一算一次diff.防止刷新多次diff.lastbook.
        self.NewV = mean.GetPredictP(bookL[:])     #统一算一次NewV  Mean
    
    def GetAvgLot(self):
        AvgLot = utlist.AvgLotL(self.BookL[:])*1.5 #破位信号总量
        return AvgLot 
