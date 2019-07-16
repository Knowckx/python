
# experience args
RecnetBarsLen = 100
ExtmCheckLen = 20

class DvgSet:
    def __init__(self, df, f_hl):  # given a invaild block
        self.DF = df  # target df datas
        self.F_hl = f_hl
        self.BlockL5 = Block()  # P1
        self.BlockL10 = Block()  # P2
        self.DvgSignal = DvgSignal()  # P3

    # P1 P2
    def Go(self):
        self.GetBlockL5()
        if self.BlockL5.IsInValid():
            return -1

        self.GetBlockL10()  # only L5 is TypeB is Possible

        self.FinalLog()
        return 1

    # P1 dig Block L5
    def GetBlockL5(self):
        dfRecent = self.DF[-RecnetBarsLen:]
        self.BlockL5 = self.DigBlockWithPoint(dfRecent)
        self.BlockL5.Anal(self.F_hl)

    # func1 given index_right,given ask [high,1,red or low,-1,green] to find the wholeblock
    # return the block with DF[left , right]
    def DigBlockWithPoint(self, df):
        tempbok = Block()
        clList = df.close[-ExtmCheckLen:]
        idxTar = clList.idxmax()
        h_l = self.F_hl
        if h_l == -1:
            idxTar = clList.idxmin()
        mv = df.loc[idxTar, 'macd']
        if (h_l == 1 and mv < 0) or (h_l == -1 and mv > 0):
            tempbok.Init(idxTar, idxTar, df)
            print("not sync. block is a point")
            return tempbok
        return self.DigCommonBlock(df)

    def DigCommonBlock(self, df):
        tempbok = Block()
        lastI = df.index[-1]
        tempRi = self.GetNextBlockRight(df.macd, lastI)
        tempLe = self.GetBlockLeft(df.macd, tempRi)
        tempbok.Init(tempLe, tempRi, df)
        return tempbok

    # UT [ ,X]
    def GetNextBlockRight(self, macdList, lastI):
        f_hl = self.F_hl
        i = lastI
        while i > 0:
            if (f_hl == 1 and macdList[i] > 0) or (f_hl == -1 and macdList[i] < 0):
                return i
            i -= 1

    # UT [x,right]
    def GetBlockLeft(self, macdList, right):
        f_hl = self.F_hl
        i = right
        while i > 0:
            if (f_hl < 0 and macdList[i] < 0) or (f_hl > 0 and macdList[i] > 0):
                i -= 1
                continue
            # > 0
            return i+1
        msg = "GetLeftofBlock1 Error:Index Out of the Array"
        print(msg)
        return -1

    # 给出符合长度的block
    def GetBlockL10(self):
        idxNow = self.BlockL5.ILe-1
        df = self.DF.loc[:idxNow]
        maxTry = 3  # 参见2018-06出现的间杂点
        maxBars = 40  # 向前寻找最多2个月*20天
        while maxTry > 0 and maxBars > 0:
            tempRi = self.GetNextBlockRight(df.macd, idxNow)  # 1
            maxBars -= (idxNow - tempRi)
            if maxBars < 0:
                break
            tempLe = self.GetBlockLeft(df.macd, tempRi)
            tempLen = tempRi-tempLe+1
            if tempLen >= 0.8*self.BlockL5.Len():
                # success
                self.BlockL10.Init(tempLe, tempRi, df)
                self.BlockL10.Anal(self.F_hl)
                return 
            maxTry -= 1
            maxBars -= tempLen
            idxNow = tempLe - 1
        return 

    def FinalLog(self):
        bokL5 = self.BlockL5
        bokL10 = self.BlockL10

        mod = ""
        if not bokL10.IsInValid():
            mSet = DvgSignal()
            mSet.InitBlock2(bokL10.RepUn, bokL5.RepUn, self.F_hl)
            rst = mSet.IsDvg()
            if rst:
                # print("find Block Dvg")
                mSet.Print()
                mod = "2.0 -- "

        if bokL5.TyB:
            # print("find L5 TypeB Dvg")
            bokL5.TyB_Set.Print()
            mod = mod + "1.1"
        else:
            if mod != "":
                mod = mod + "1.0"

        if mod == "":
            print("<--- None Out")
        else:
            print("Anal result:%s"%mod)
            print("<--- Success")
        return


#　obj represent macd Block
class Block:
    def __init__(self):  # given a invaild block
        self.ILe = -1  # base info
        self.IRi = -1

        self.TyB = False  # Dvg.TyB in the Block
        self.RepUn = DvgUnit()  # the DvgUnit of this Block

    def IsInValid(self):
        if self.ILe == -1 or self.IRi == -1:
            return True
        return False

    def Init(self, ile, iri, df):
        self.ILe = ile
        self.IRi = iri
        self.DF = df.loc[ile:iri]
        # print(newDF)

    # Known [ILe,IRr] Anal and filled Values
    def Anal(self, f_hl):
        df = self.DF
        if f_hl == 0:
            return

        self.TLe = self.DF.loc[self.ILe,"time"]
        self.TRi = self.DF.loc[self.IRi,"time"]

        idxP = df.close.idxmin()  # f_hl = -1
        idxM = df.macd.idxmin()
        if f_hl == 1:
            idxP = df.close.idxmax()
            idxM = df.macd.idxmax()
        self.RepUn.Init(df, idxP)  # 总是由极值代表
        if idxP == idxM:
            # print("Block Desc:Single extm")
            return

        # Try TyB  价格极值总是在右边
        # print("try check TyB:%s %s"%(DFTime(df,idxM), DFTime(df,idxP)))
        dvgSignal = DvgSignal()
        dvgSignal.InitPoint2(df, idxM, idxP, f_hl)
        if dvgSignal.IsDvg():
            self.TyB = True
            self.TyB_Set = dvgSignal
        return

    def Len(self):
        return (self.IRi - self.ILe + 1)

    def Print(self):
        df = self.DF
        print("Block [%s,%s]" % (DFTime(df, self.ILe), DFTime(df, self.IRi)))


# 判断背离
class DvgSignal:
    def __init__(self):
        self.LU = DvgUnit()
        self.RU = DvgUnit()
        self.F_hl = 0

    # two point
    def InitPoint2(self, df, idxL, idxR, f_hl):
        self.LU.Init(df, idxL)
        self.RU.Init(df, idxR)
        self.F_hl = f_hl

    def InitBlock2(self, lu, ru, f_hl):
        self.LU = lu
        self.RU = ru
        self.F_hl = f_hl

    def IsDvg(self):
        f_hl = self.F_hl
        if f_hl == 1:  # red
            if self.RU.Pv >= self.LU.Pv and self.RU.Mv <= self.LU.Mv:
                return True
        if f_hl == -1:
            if self.RU.Pv <= self.LU.Pv and self.RU.Mv >= self.LU.Mv:
                return True
        return False

    def Print(self):
        print("DvgSignal:[%s %s]" % (self.LU.Time, self.RU.Time))


class DvgUnit:
    def __init__(self):
        self.Idx = -1
        self.Pv = 0.0
        self.Mv = 0.0
        self.Time = ""

    def Init(self, df, idx):
        self.Idx = idx
        self.Pv = df.loc[idx, 'close']
        self.Mv = df.loc[idx, 'macd']
        self.Time = df.loc[idx, 'time']


# ----------------- struct -----------------
class ExtmCheckRst:
    def __init__(self):
        self.F_hl = 0
        self.Idx = -1

    def __init__(self, checkRst, idx):
        self.F_hl = checkRst
        self.Idx = idx


# ----------------- Func -----------------


def DFTime(df, idx):
    return df.loc[idx, 'time']
