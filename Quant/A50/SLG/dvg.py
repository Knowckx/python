import pandas as pd
import logging
import datetime

# from .c_dvg import *

'''
Divergence [daɪˈvɜːrdʒəns] 
分歧 背离
'''

# logger
def GetLogHandle():
    logger = logging.getLogger("de")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    return logger

logger = GetLogHandle()

# -----------------Main Start-----------------

# 入口
def Start(df,grade = "1d"):
    SetGradeFixPara(grade)
    # pre is lowest or highest
    rst = IsExtmAndTurn(df.close)
    if rst.F_hl == 0:
        # logger.info("IsExtmAndTurn false,continue")
        return DvgRst()
    
    # 此时[-2]位置一定是极值！
    dvg = DvgSet(df,rst.F_hl)
    dvgrst = dvg.Go()
    # logger.info(dvgrst)
    return dvgrst

# DVG判断修正参数,防止接近新高但是未到，却背离的情况
DvgExtmFixPara = 0.0018 
def SetGradeFixPara(grade):
    global DvgExtmFixPara
    default = DvgExtmFixPara
    if grade == "1d":
        DvgExtmFixPara = default
    if grade == "60m":
        DvgExtmFixPara = default/2
    if grade == "15m":
        DvgExtmFixPara = default/2/2
    if grade == "5m":
        DvgExtmFixPara = default/2/2/1.5

# price now is extremum and turn  va -1 lowest 1 hight 0 normal
def IsExtmAndTurn(clList):
    closeList = clList[-ExtmCheckLen:]
    taridx = closeList.index[-2]
    tarP = closeList.iat[-2]
    minP = closeList.min()
    if tarP <= minP*(1 + DvgExtmFixPara): # low
        return ExtmCheckRst(-1, taridx)
    maxP = closeList.max()
    if tarP >= maxP*(1 - DvgExtmFixPara):
        return ExtmCheckRst(1, taridx)
    return ExtmCheckRst(0, -1)



# --------------------------------------------Class区--------------------------------------------

# experience args
RecnetBarsLen = 100
ExtmCheckLen = 20 # #20天差不多了，上涨中的回调产生的背离大概间隔20天



class DvgSet:
    def __init__(self, df, f_hl):  # given a invaild block
        self.DF = df  # target df datas
        self.F_hl = f_hl
        self.BlockL5 = Block()  # P1
        self.BlockL10 = Block()  # P2
        self.DvgSignal = DvgSignal()  # P3

    # P1 P2
    def Go(self):
        rstL5 = self.GetBlockL5()
        if rstL5 == False:
            return DvgRst()
        self.GetBlockL10()  # only L5 is TypeB is Possible

        return self.FinalLog()

    # P1 dig Block L5
    def GetBlockL5(self):
        dfRecent = self.DF[-RecnetBarsLen:]
        bok = self.DigBlockWithPoint(dfRecent)
        if bok.IsValid() == False:
            return False
        bok.Anal(self.F_hl)
        self.BlockL5 = bok

    # func1 given index_right,given ask [high,1,red or low,-1,green] to find the wholeblock
    # return the block with DF[left , right]
    def DigBlockWithPoint(self, df):
        tempbok = Block()
        clList = df.close[-ExtmCheckLen:] 
        h_l = self.F_hl
        idxTar = clList.index[-2] #默认[-2]位置是极值。因为前面已经有检查

        # GN02 剔除反向段。 
        if h_l == -1: 
            if df.macd.at[idxTar-1] < df.macd.at[idxTar]: #背离点的M值必须更小
                return tempbok
        if h_l == 1: 
            if df.macd.at[idxTar-1] > df.macd.at[idxTar]: #背离点的M值必须更小
                return tempbok

        # 先检查一下，是否是 单点背离 - 反色 的形态
        mv = df.loc[idxTar, 'macd']
        if (h_l == 1 and mv < 0) or (h_l == -1 and mv > 0):
            tempbok.Init(idxTar, idxTar, df)
            # logger.info("not sync. block is a point")
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
        logger.info(msg)
        return -1

    # 给出符合长度的block
    def GetBlockL10(self):
        idxNow = self.BlockL5.ILe-1
        df = self.DF.loc[:idxNow]
        maxTry = 3  # 参见2018-06出现的间杂点
        maxSearchBars = 40  # 向前寻找最多2个月*20天
        while maxTry > 0 and maxSearchBars > 0:
            tempRi = self.GetNextBlockRight(df.macd, idxNow)  # 1
            maxSearchBars -= (idxNow - tempRi)
            if maxSearchBars < 0:
                break
            tempLe = self.GetBlockLeft(df.macd, tempRi) # 目标块的左右都已拿到
            tempLen = tempRi-tempLe+1
            if tempLen >= 0.8*self.BlockL5.Len(): # 长度要合格
                # success
                self.BlockL10.Init(tempLe, tempRi, df)
                self.BlockL10.Anal(self.F_hl)
                return 
            maxTry -= 1
            maxSearchBars -= tempLen
            idxNow = tempLe - 1
        return 

    # L10是否有效
    def IsBokL10Valid(self):
        bokL5 = self.BlockL5
        bokL10 = self.BlockL10
        if not bokL10.IsValid():
            return False
        f_hl = self.F_hl
        if f_hl == 1:  # red
            if bokL10.Mv <= bokL5.Mv:
                return False
        if f_hl == -1:
            if bokL10.Mv >= bokL5.Mv:
                return False
        return True

    def FinalLog(self):
        bokL5 = self.BlockL5
        bokL10 = self.BlockL10

        modL,modR = "",""

        mSet = DvgSignal()
        mRst = DvgRst()

        if self.IsBokL10Valid(): # 是否是标准的双块背离呢
            mSet.InitBlock2(bokL10.RepUn, bokL5.RepUn, self.F_hl)
            rst = mSet.IsDvg()
            if rst:  
                modL = "10"  # 默认简单双块背离
                modR = "5"

            rst2 = mSet.IsDvgPatchTypeA()
            if rst2 == False:
                modL = "10(Filter)" # 左侧被过滤掉了
                modR = ""

        if bokL5.SetTyB.OK:
            modR = "5.2" # 右侧是块内背离！

        if modL == "" and modR == "":
            return mRst


        dvgTime = self.DF.time.iat[-1]
        modmsg  = modL + " " + modR

        if modL == "10(Filter)" and modR == "": #虽然背离，但是被过滤了
            msg = "---> time:{} msg:{} Pass!\n".format(dvgTime,modmsg)
            logger.info(msg)
            return mRst

        # 看来是有效的
        mRst.F_hl = self.F_hl
        mRst.Time = dvgTime
        mRst.Mode = modmsg
        mRst.Detail = "{} {}".format(mSet.String(),bokL5.SetTyB.String())
        return mRst



#　obj represent macd Block
class Block:
    def __init__(self):  # given a invaild block
        self.ILe = -1  # base info
        self.IRi = -1

        self.SetTyB = DvgSignal()  # TyB in the Block
        self.RepUn = DvgUnit()  # the DvgUnit of this Block

    def IsValid(self):
        if self.ILe != -1 and self.IRi != -1:
            return True
        return False

    def Init(self, ile, iri, df):
        self.ILe = ile
        self.IRi = iri
        self.DF = df.loc[ile:iri]
        # logger.info(newDF)

    # Known [ILe,IRr] Anal and filled Values
    def Anal(self, f_hl):
        df = self.DF
        if f_hl == 0:
            return

        self.TLe = df.loc[self.ILe,"time"]
        self.TRi = df.loc[self.IRi,"time"]

        idxP,idxM = 0,0
        if f_hl == -1:
            idxP = df.close.idxmin()  # if f_hl = -1
            idxM = df.macd.idxmin()
        if f_hl == 1:
            idxP = df.close.idxmax()
            idxM = df.macd.idxmax()

        self.Mv = self.DF.loc[idxM,"macd"] # 保存一下本块的MACD极值
        self.RepUn.Init(df, idxP)  # 总是由极值代表
        if idxP == idxM:
            # logger.info("Block Desc:Single extm")
            return

        # Try TyB  
        self.SetTyB.InitPoint2(df, idxM, idxP, f_hl)
        self.SetTyB.IsDvg()
        return

    def Len(self):
        return (self.IRi - self.ILe + 1)

    def Print(self):
        df = self.DF
        logger.info("Block [%s,%s]" % (DFTime(df, self.ILe), DFTime(df, self.IRi)))


# 判断背离
class DvgSignal:
    def __init__(self):
        self.LU = DvgUnit()
        self.RU = DvgUnit()
        self.F_hl = 0
        self.OK = False

    # two point
    def InitPoint2(self, df, idxL, idxR, f_hl):
        if idxL > idxR: # 价值极值总在右边
            return
        self.LU.Init(df, idxL)
        self.RU.Init(df, idxR)
        self.F_hl = f_hl

    # typeA类型的背离
    def InitBlock2(self, lu, ru, f_hl):
        self.LU = lu
        self.RU = ru
        self.F_hl = f_hl
        self.Type = "TypeA"
    
    # GN03
    def IsDvgPatchTypeA(self):
        if self.Type != "TypeA":
            return True #默认背离有效
        AvgL = (self.LU.Mdea + self.LU.Mdif)/2
        AvgR = (self.RU.Mdea + self.RU.Mdif)/2
        if (AvgR*AvgL)>0 and abs(AvgL) < abs(AvgR):
            return False
        return True


    def IsDvg(self):
        f_hl = self.F_hl
        if f_hl == 1:  # red
            if self.RU.Pv >= self.LU.Pv*(1 - DvgExtmFixPara) and self.RU.Mv <= self.LU.Mv:
                self.OK = True
                self.Rate = round(self.RU.Mv/self.LU.Mv,3)
        if f_hl == -1:
            if self.RU.Pv <= self.LU.Pv*(1 + DvgExtmFixPara) and self.RU.Mv >= self.LU.Mv:
                self.OK = True
                self.Rate = round(self.RU.Mv/self.LU.Mv,3)
        return self.OK

    def Print(self):
        self.String()

    def String(self):
        ss = ""
        if self.OK:
            ss = "[L,{} R,{} rate,{}]".format(self.LU.Time, self.RU.Time,self.Rate)
        return ss

# 该块用于比较的那个点位
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
        self.Mdea = df.loc[idx, 'dea']
        self.Mdif = df.loc[idx, 'dif']


# ----------------- struct -----------------
class ExtmCheckRst:
    def __init__(self):
        self.F_hl = 0
        self.Idx = -1

    def __init__(self, checkRst, idx):
        self.F_hl = checkRst
        self.Idx = idx

# 表达背离结果
class DvgRst:
    def __init__(self):
        self.F_hl = 0  # 背离信号类别 0表示非背离
        self.Time = "" # 时间
        self.Mode = "" # 模式
        self.Detail = "" # 详细点位
    
    def ToPyTime(self):
        year_s, mon_s, day_s = self.Time.split('-')
        self.Time = datetime.datetime(int(year_s), int(mon_s), int(day_s))

    def IsSame(self,inRst):
        inRst.ToPyTime()
        if inRst.F_hl == self.F_hl and inRst.Time == self.Time:
            return True
        return False


    def String(self):
        return "time:{} flag:{}".format(self.Time,self.F_hl)

    def Print(self):
        logger.info(self.String())
        # logger.info(" || mode:{}".format(,self.Mode))
        logger.info(self.Detail)
        logger.info("\n")

# ----------------- Func -----------------


def DFTime(df, idx):
    return df.loc[idx, 'time']
