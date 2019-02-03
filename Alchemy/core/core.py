from Alchemy.core import c_signset,c_book,c_box
from bookut import utlist



class Core:
    def __init__(self,maxGap = 1):
        # self.MaxGap = maxGap
        self.SignH = c_signset.Signal(1)
        self.SignL = c_signset.Signal(-1)
        self.Box = c_box.CBox()
        self.histyL = [] # 记录历史上的决策
        # self.Str = ["High","Low"]

    def PutNew(self,bookL,HisI):
        self.Book = c_book.CBook(bookL,HisI)

        # 初始状态 两个都是false
        if (not self.SignH.IsOpen()) and (not self.SignL.IsOpen()):
            self.SignH.Reset(self.Book)
            self.SignL.Reset(self.Book)
            return

        for Type in [-1,1]:
            code = self.Update(Type)
            if code == 1:
                break

    def Update(self,Type):
        sighSetA,sighSetB = self.SignH,self.SignL
        strA,strB = "High","Low"
        if Type == -1:
            sighSetA,sighSetB = sighSetB,sighSetA
            strA,strB = strB,strA
        print("SignSet %s:"%(strA))
        statusCode = sighSetA.Update(self.Book) # 判断..
        if statusCode == 501 or statusCode == 502: #Signal is Closed || reset
            return None

        print("result:%d"%(statusCode))
        if statusCode == 1:  # 确定是个信号
            ii,vv = sighSetA.GetHisEx()
            sighSetA.Close()
            sighSetB.Reset(self.Book)

            if self.CheckBox(vv):
                print("Box say no")
                return None
            self.addHis([ii,vv])
            return 1

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
    
    def CheckBox(self,vv):
        return self.Box.NewValue(vv.V())


# 两数差值的百分比
def GetDifPst(v1,v2):
    dw = v1.V()
    dif = (v2 - v1)/dw*100
    return round(dif,2)



