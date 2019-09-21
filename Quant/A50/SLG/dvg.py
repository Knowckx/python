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


# -----------------Init -----------------
logger = GetLogHandle()


# DVG判断修正参数,防止接近新高但是未到，却背离的情况
DvgExtmFixPara = 0.0018 
Dvg02Para = 0.025  # DVG02 股价形成非常狭窄的通道时，不再进行背离运算
def SetGradeFixPara(grade):
    global DvgExtmFixPara
    global Dvg02Para
    fixed = 1
    if grade == "1d":
        fixed = 1
    if grade == "60m":
        fixed = 2
    if grade == "15m":
        fixed = 2*2
    if grade == "5m":
        fixed = 2*2*1.5 # 就是6
    DvgExtmFixPara = DvgExtmFixPara/fixed
    Dvg02Para = Dvg02Para/fixed

# 这个包需要手动初始化一次
def Init(grade):
    SetGradeFixPara(grade)
    # print(Dvg02Para)
# -----------------Main Start-----------------

# 入口
def Start(df):
    debugP = '2019-09-18 11:10:00'
    if df.time.iloc[-1] == debugP:
        print("debug at" + debugP)
    rst = EnterCheck(df)
    if rst == False:
        return DvgRst()

    F_hl = IsExtmAndTurn(df.close)
    if F_hl == 0:
        return DvgRst()

    dvg = DvgSet(df,F_hl)
    dvgrst = dvg.Go()
    # logger.info(dvgrst)
    return dvgrst

def EnterCheck(df):
    return Enter02(df) and Enter03(df)

# 道理太窄，背离已经先去意义
def Enter02(df):
    bollgap = df.bup.iat[-1] - df.blow.iat[-1]
    # rst = DvgRst()
    if (bollgap/df.blow.iat[-1] < Dvg02Para):
        # print("Dvg02 通道过窄,pass")
        return False
    return True

# 不准MACD还在继续开口。
def Enter03(df):
    v1 = df.macd.iat[-1] # 右
    v2 = df.macd.iat[-2] # 左
    if abs(v2) <= abs(v1):
        return False
    return True
        


# 入口 极值检查   
# 目前使用 倒数第二天的价格必须是极值
def IsExtmAndTurn(clList):
    closeList = clList[-ExtmCheckLen:] # 收盘价数组
    flag = 0
    tarP1 = closeList.iat[-1]  # 最近两天的价格与坐标
    idxP1 =  closeList.index[-1]
    tarP2 = closeList.iat[-2] 
    idxP2 =  closeList.index[-2]

    localList = closeList[-ExtmCheckLen:-2] #不包含今天和昨天
    # print(len(closeList))
    # print(closeList[-5:])   

    
    minidx = localList.idxmin() #不包含今天和昨天
    fixminP = localList.loc[minidx]*(1 + DvgExtmFixPara)

    # 希望昨天是个低值  同时今天比昨天要缓和
    if tarP2 <= fixminP and tarP1 >= tarP2*(1 - DvgExtmFixPara):
        return -1

    # 最大值的情况下
    maxidx = localList.idxmax()
    fixmaxP = localList.loc[maxidx]*(1 - DvgExtmFixPara)
    if tarP2 >= fixmaxP and tarP1 <= tarP2*(1 + DvgExtmFixPara):
        return 1
    return 0

# --------------------------------------------Class区--------------------------------------------

# 经验参数
RecnetBarsLen = 100
ExtmCheckLen = 20 # #20天差不多了，上涨中的回调产生的背离大概间隔20天



class DvgSet:
    def __init__(self, df, f_hl):  # given a invaild block
        self.DF = df  # target df datas
        self.F_hl = f_hl
        self.BlockL5 = Block()  # 块内背离在这里检查
        self.BlockL10 = Block() 
        self.TyASet = DvgSignal() # 双块背离的检查
        self.DvgRst = DvgRst() # 本次背离的判断结果

    # P1 P2
    def Go(self):
        rstL5 = self.GetBlockL5()
        if rstL5 == False:
            return DvgRst()
        self.GetBlockL10()
        self.BaseLog()
        self.PatchLog()
        return self.DvgRst

    # P1 dig Block L5
    def GetBlockL5(self):
        dfRecent = self.DF[-RecnetBarsLen:]
        bok = self.DigBokRiWithPoint(dfRecent)
        if bok.IsValid() == False:
            return False
        bok.Anal(self.F_hl)
        self.BlockL5 = bok

    # func1 given index_right,given ask [high,1,red or low,-1,green] to find the wholeblock
    # 鉴定右块的左右边界 
    def DigBokRiWithPoint(self, df):
        tempbok = Block()
        h_l = self.F_hl
        # 是否是 单点背离 - 反色 的形态
        idxTar = GetBokRiLocalExtm(df,h_l)
        mv = df.loc[idxTar, 'macd']
        if (h_l == 1 and mv < 0) or (h_l == -1 and mv > 0):
            tempbok.Init(idxTar, idxTar, df)
            # logger.info("not sync. block is a point")
            return tempbok
        # 普通的块背离
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

    # 尝试寻找左块 - 非必须
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

    # 基础背离判断
    def BaseLog(self):
        self.DvgRst = DvgRst() # 本函数返回的结果集
        bokL5 = self.BlockL5
        bokL10 = self.BlockL10
        modL,modR = "",""

        # 进入基础判断
        if self.BlockL10.IsValid(): # 左块是有效的话
            # self.TyASet.InitBlock2(bokL10.RepUn, bokL5.RepUn, self.F_hl)
            self.TyASet.InitPoint2(self.DF,bokL10.RepUn.Idx,bokL5.RepUn.Idx, self.F_hl)
            self.TyASet.SetType("TypeA")
            rst = self.TyASet.IsDvg()
            if rst:  
                modL = "10"  # 默认简单双块背离
                modR = "5"

        if bokL5.SetTyB.OK:
            modR = "5.2" # 右块是TyB！

        if modL == "" and modR == "": #不是背离
            return

        # 看来是有效的
        self.DvgRst.F_hl = self.F_hl
        self.DvgRst.Time = self.DF.time.iat[-1]
        self.DvgRst.Mode = modL + " " + modR
        self.DvgRst.Detail = "{} {}".format(self.TyASet.String(),bokL5.SetTyB.String())
        return 

    # 加上筛选项的进阶背离判断
    def PatchLog(self):
        if self.DvgRst.F_hl == 0:
            return
        
        if self.BlockL5.SetTyB.OK: # 本次是块内背离哦
            setTyB = self.BlockL5.SetTyB
            # if setTyB.CheckGN01() == False:
            #     self.DvgRst.Patch = "GN01"
            #     return
            if setTyB.CheckDvg13() == False:
                self.DvgRst.Patch = "Dvg13"
                return



        # self.BlockL5.

        # self.DvgRst.IsSame
                    # rst2 = mSet.IsDvgPatchTypeA()
            # if rst2 == False:
            #     modL = "10(Filter)" # 左侧被过滤掉了
            #     modR = ""



        # dvgTime = self.DF.time.iat[-1]
        # modmsg  = modL + " " + modR

        # if modL == "10(Filter)" and modR == "": #虽然背离，但是被过滤了
        #     msg = "---> time:{} msg:{} Pass!\n".format(dvgTime,modmsg)
        #     logger.info(msg)
        #     return mRst



#　代表一个背离的颜色块
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

        clList = df.close.loc[self.ILe:self.IRi]
        idxP = clList.idxmax() 
        if f_hl == -1:
            idxP = clList.idxmin()
        self.RepUn.Init(df, idxP)    # 本块总是由价格极值代表

        # 向左找的较大点的M块极值点
        idxM = idxP - 1
        while (idxM > self.ILe):
            tempLis = df.macd.loc[idxM-3:idxM+1]
            # print(tempLis)
            temp = 0
            if f_hl == -1:
                temp = tempLis.idxmin()
            if f_hl == 1:
                temp = tempLis.idxmax()
            if temp == idxM:
                break
            if temp < idxM:
                idxM = temp
            else:
                idxM -= 1  # 左移动
        # print(df.loc[idxM,"time"])
        self.Mv = self.DF.loc[idxM,"macd"] # 保存一下本块的MACD极值
        
        if idxP == idxM:
            # logger.info("Block Desc:Single extm")
            return

        # 检查TyB的块内背离
        self.SetTyB.InitPoint2(df, idxM, idxP, f_hl)
        self.SetTyB.IsDvg()
        return

    def Len(self):
        return (self.IRi - self.ILe + 1)

    def Print(self):
        df = self.DF
        logger.info("Block [%s,%s]" % (DFTime(df, self.ILe), DFTime(df, self.IRi)))


# 放入两点，准备来判断背离
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
        self.DF = df

    def SetType(self,ty):
        self.Type = ty

    # GN01 块内背离的两点,M线值必须同正负
    def CheckGN01(self):
        AvgMvL = (self.LU.Mdea + self.LU.Mdif)/2
        AvgMvR = (self.RU.Mdea + self.RU.Mdif)/2
        if (AvgMvL*AvgMvR) < 0: 
            return False
        return True
    

    # Dvg13 对于反向段来说，我们希望M块的rate要合格
    def CheckDvg13(self):
        if self.RU.Idx - self.LU.Idx== 1: # 相临两点的，一定是无效（在5M级别）
            return False
        
        isReverse = self.CheckIsReverse() 
        if isReverse == False:
            return True # 通过
        # 是反向段哦
        if self.Rate < 0.5:
            return True # 通过
        return False
    
    # 是不是反向段呢？
    def CheckIsReverse(self):
        df = self.DF
        rRepV = df.loc[self.RU.Idx, 'repv'] 
        lRepV = df.loc[self.LU.Idx, 'repv'] 
        midIdx = round((self.LU.Idx+self.RU.Idx)/2)
        mRepV = df.loc[midIdx, 'repv'] 

        m1 = df.macd.iat[-2]
        m2 = df.macd.iat[-3]
        m3 = df.macd.iat[-4]
        # 这说明没有形成突点，M块一直在回归
        if abs(m3) > abs(m2) and abs(m2) > abs(m1):
            return True
        if self.F_hl == 1:
            if lRepV < mRepV and mRepV < rRepV:
                return True
        if self.F_hl == -1 and lRepV > mRepV and mRepV > rRepV:
            return True
        return False

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

# 表达背离结果
class DvgRst:
    def __init__(self):
        self.F_hl = 0  # 背离信号类别 0表示非背离
        self.Time = "" # 时间
        self.Mode = "" # 模式
        self.Detail = "" # 详细点位
        self.Patch = "" # 附加检查
    
    def ToPyTime(self):
        FormatDate = "%Y-%m-%d %H:%M:%S"
        if len(self.Time) == 10:
            FormatDate = "%Y-%m-%d"
        self.Time = datetime.datetime.strptime(self.Time, FormatDate)

    def IsSame(self,inRst):
        if inRst.F_hl == 0:
            return False
        # self.ToPyTime()
        b1 = inRst.F_hl == self.F_hl
        b2 = inRst.Time == self.Time
        b3 = (inRst.Patch == "" and self.Patch == "" ) or (inRst.Patch != "" and self.Patch != "" ) 
        if b1 and b2 and b3:
            return True
        return False


    def String(self):
        return "time:{} flag:{}".format(self.Time,self.F_hl)

    def Print(self):
        logger.info(self.String())
        # logger.info(" || mode:{}".format(,self.Mode))
        logger.info(self.Detail + self.Patch)
        # logger.info("\n")

# ----------------- Func -----------------


def DFTime(df, idx):
    return df.loc[idx, 'time']


# 最近的两个点中，实际被选出的点的idx
def GetBokRiLocalExtm(df,h_l):
    clList = df.close[-2:]  # 在我们的模型中，最近两个bar一定有一个代表点
    idxTar = clList.idxmax() 
    if h_l == -1:
        idxTar = clList.idxmin()
    return idxTar
#--------------------------------------------保留的功能区
# def test():




    
#     if modL == "10(Filter)" and modR == "": #虽然背离，但是被过滤了
#         msg = "---> time:{} msg:{} Pass!\n".format(dvgTime,modmsg)
#         logger.info(msg)
#         return mRst


            # rst2 = mSet.IsDvgPatchTypeA()
            # if rst2 == False:
            #     modL = "10(Filter)" # 左侧被过滤掉了
            #     modR = ""