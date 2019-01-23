from Alchemy.core import c_signset,c_book
from bookut import utlist


class Core:
    def __init__(self,maxGap = 1):
        # self.MaxGap = maxGap
        self.SignH = c_signset.Signal(1)
        self.SignL = c_signset.Signal(-1)
        self.histyL = [] # 记录历史上的决策

    def PutNew(self,bookL,HisI):
        self.Book = c_book.CBook(bookL,HisI)

        # 初始状态 两个都是false
        if (not self.SignH.IsOpen()) and (not self.SignL.IsOpen()):
            self.SignH.Reset(self.Book)
            self.SignL.Reset(self.Book)
            return

        k = self.UpdateH()
        if k == -1:#H先reset，会导致L会更新此次
            return
        self.UpdateL()
        # print('prc %s  his: %s %s'%(self.Nprc,self.Low,self.High))

     # 峰值，要不要sell?
    def UpdateH(self):
        # self.SignH.Sync(self.Book)
        statusCode = self.SignH.Update(self.Book) # 判断..
        if statusCode == 501: #Signal is Closed
            return 
        print("try update Sign High")
        print("High.Update Result :",statusCode)
        if statusCode == 1:  # 确定是个高点回落信号
            self.addHis(self.SignH.GetHisEx())
            self.SignH.Close()
            self.SignL.Reset(self.Book)
            return -1

    # 低值，要不要buy?
    def UpdateL(self):
        # self.SignH.Sync(self.diff,self.NewV)
        statusCode = self.SignL.Update(self.Book)
        if statusCode == 501: #Signal is Closed
            return
        print("try update Sign low")
        print("Sign Low:",statusCode)
        if statusCode == -1:
            self.addHis(self.SignL.GetHisEx())
            self.SignL.Close()
            self.SignH.Reset(self.Book)

    # def PrintStatus(self):
    #     print("high and low:",self.High,self.Low)
    #     print("Sign high and low:",self.SignH,self.SignL)


    def addHis(self,Li):
        L = utlist.TupleToList(Li)
        hisL = self.histyL
        if len(hisL) > 0:
            last = hisL[-1] #上一次的极点
            dif = GetDifPst(last[1],L[1]) #
            last.append(dif)
        self.histyL.append(L)

    def DumpHisty(self):
        print("DumpCoreHisty:")
        for his in self.histyL:
            ss = '%d : %s' % (his[0],his[1])
            if len(his) == 3:
                ss= '%s,%s%%' % (ss,his[2])
            print(ss)
            

# 两数差值的百分比
def GetDifPst(v1,v2):
    dw = v1.V()
    dif = (v2 - v1)/dw*100
    return round(dif,2)



