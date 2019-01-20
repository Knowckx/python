from bookut import mean,utlist
from .signset import *
# from signal import *


class Core:
    def __init__(self,maxGap = 1):
        # self.MaxGap = maxGap
        self.SignH = Signal(1)
        self.SignL = Signal(-1)
        self.histyL = [] # 记录历史上的决策

    def PutNew(self,bookL,HisI):
        self.HisI = HisI # 极点值的序号
        self.HisB = bookL

        self.UpdateH()
        self.UpdateL()
        # print('prc %s  his: %s %s'%(self.Nprc,self.Low,self.High))

     # 峰值，要不要sell?
    def UpdateH(self):
        ok,ss = self.SignH.Update(self.HisB,self.HisI) # 判断..
        if ss == '500': #Signal is Closed
            return
        print("try update Sign High")
        print("Sign High:",ok,ss)
        if ok:  # 确定是个高点回落信号
            self.addHis(self.SignH.GetHisEx())
            self.SignH.Close()
            self.SignL.Reset()

    # 低值，要不要buy?
    def UpdateL(self):
        ok,ss = self.SignL.Update(self.HisB,self.HisI)
        if ss == '500': #Signal is Closed
            return
        print("try update Sign low")
        print("Sign Low:",ok,ss)
        if ok:
            self.addHis(self.SignL.GetHisEx())
            self.SignL.Close()
            self.SignH.Reset()


    # def PrintStatus(self):
    #     print("high and low:",self.High,self.Low)
    #     print("Sign high and low:",self.SignH,self.SignL)


    def DumpHisty():
        print("DumpHisty:")
        for his in histyL:
            print('%d at %s' % (his[1],his[0]))

    def addHis(self,L):
        hisL = self.histyL
        if len(hisL) > 0:
            last = hisL[-1]
            dif = GetDifPst(last[1],L[1])
            last.append(dif)
        self.histyL.append(L)



# 两数差值的百分比
def GetDifPst(v1,v2):
    dif = (v2 - v1)/v1*100
    return round(dif,2)

def TupleToList(tu):
    rst = []
    for t in tu:
        rst.append(t)
    return rst


