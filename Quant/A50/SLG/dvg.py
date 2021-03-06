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
ChanEnter01Para = 2.5  # DVG02 股价形成非常狭窄的通道时，不再进行背离运算
def SetGradeFixPara(grade):
    global DvgExtmFixPara
    global ChanEnter01Para
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
    ChanEnter01Para = ChanEnter01Para/fixed

# 这个包需要手动初始化一次
def Init(grade):
    SetGradeFixPara(grade)
    # print(ChanEnter01Para)
# -----------------Main Start-----------------

def DebugAt(df,debugP):
    if debugP == "":
        return
    print("now is:" + df.time.iat[-1])
    if df.time.iloc[-1] == debugP:
        print("debug at:" + debugP)
        logger.setLevel(logging.DEBUG) # 可以打印


# 入口
def Start(df):
    DebugAt(df,'2019-10-21 10:00:00')
    # 先检查通道模式
    # chSign = Channel()
    # rst = chSign.Go(df)
    # if rst.Type != "": # 说明已经处于通道模式了
    #     return rst

    # 有需要再检查dvg模式
    rst = EnterCheck(df)
    if rst.F_hl == 0:
        return rst

    dvg = DvgSet(df,rst.F_hl)
    rst = dvg.Go()
    # logger.info(JudgeRst)
    return rst

def EnterCheck(df):
    rst = JudgeRst()
    flag = IsExtmAndTurn(df) # step1,大概得到flag
    if flag == 0:
        return rst
    logger.debug("EnterCheck get flag:{}".format(flag))

    if not Enter03(df,flag):
        return rst

    rst.F_hl = flag # ok了
    return  rst



# 不准MACD还在继续开口。
def Enter03(df,flag):
    le = df.macd.iat[-2] # 左
    fixLe = le*(1+0.01)  # 允许右值大一丢丢
    ri = df.macd.iat[-1] # 右
    if flag == -1:
        return ri > fixLe
    elif flag == 1:
        return ri < fixLe
    return False
        




# 入口 极值检查   
# 目前使用 倒数第二天的价格必须是极值
def IsExtmAndTurn(df):
    clList = df.close
    closeList = clList[-ExtmCheckLen:] # 收盘价数组

    # 首先，大体判断，昨天的价格必须是最近的大概极限值位置
    flag = 0 
    tarP2 = closeList.iat[-2]  # 昨天的价格
    localList = closeList[-ExtmCheckLen:-2] # 不包含今天和昨天的这一段 表示近期的局部极限值
    localMax = localList.max()
    localMin = localList.min()
    
    if tarP2-localMin > (localMax-localMin)*0.9:
        flag = 1
    elif tarP2-localMin < (localMax-localMin)*1.1:
        flag = -1

    if flag == 0: #初步判断，本次无效，不用继续了
        return flag
    
    tarP2 = getFixRepClose(flag,df,tarP2)

    tarP1 = closeList.iat[-1]  # 今天的价格
    if flag == 1: # 高位的情况
        fixmaxP = localMax*(1 - DvgExtmFixPara)
        # 昨天的价格很高 同时今天缓和了
        if tarP2 >= fixmaxP and tarP1 <= tarP2*(1 + DvgExtmFixPara):
            return 1
    elif flag == -1:
        fixminP = localMin*(1 + DvgExtmFixPara)    
        # 希望昨天是个低值  同时今天比昨天要缓和
        if tarP2 <= fixminP and tarP1 >= tarP2*(1 - DvgExtmFixPara):
            return -1
    return 0

# 有时，今天的开盘价才是新高，需要修饰一下
def getFixRepClose(flag,df,tarP2):
    newOpen = df.open.iat[-1] #有时，今天的开盘价才是新高，修饰一下
    if flag == 1 and newOpen > tarP2:
        tarP2 = newOpen
    if flag == -1 and newOpen < tarP2:
        tarP2 = newOpen
    return tarP2


# 存在-2位置不是新高但是接近于新高。但是-1位置的开盘+最高值是新极值的情况
def GetRepP1(df):
    tarP1 = closeList.iat[-1] 



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
        self.JudgeRst = JudgeRst() # 本次背离的判断结果

    # P1 P2
    def Go(self):
        rstL5 = self.GetBlockL5()
        if rstL5 == False:
            return JudgeRst()
        self.GetBlockL10()
        self.BaseLog()
        self.PatchLog()
        return self.JudgeRst

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
        self.JudgeRst = JudgeRst() # 本函数返回的结果集
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
        self.JudgeRst.F_hl = self.F_hl
        self.JudgeRst.Time = self.DF.time.iat[-1]
        self.JudgeRst.Mode = modL + " " + modR
        self.JudgeRst.Detail = "{} {}".format(self.TyASet.String(),bokL5.SetTyB.String())
        return 

    # 加上筛选项的进阶背离判断
    def PatchLog(self):
        if self.JudgeRst.F_hl == 0:
            return

        # 单纯的typeA类型情况
        if self.BlockL5.SetTyB.OK == False: 
            if self.TyASet.IsDvgPatchTypeA() == False:
                self.JudgeRst.Patch = "PatchTypeA"
                return
            
            if self.TyASet.CheckGN04() == False:
                self.JudgeRst.Patch = "GN04"
                return

        # 本次是块内背离
        if self.BlockL5.SetTyB.OK: 
            setTyB = self.BlockL5.SetTyB
            # if setTyB.CheckGN01() == False:
            #     self.JudgeRst.Patch = "GN01"
            #     return
            if setTyB.CheckDvg13() == False:
                self.JudgeRst.Patch = "Dvg13"
                return


        

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

        idxP = 0
        clList = df.close.loc[self.ILe:self.IRi]
        if self.ILe == self.IRi:
            idxP = self.IRi
        else:
            idxP = clList.index[-2] 
        self.RepUn.Init(df, idxP)    # 本块总是由价格极值代表

        # 向左找的较大点的M块极值点
        idxM = idxP
        while (idxM > self.ILe):
            idxM -= 1
            if idxM == self.ILe+1:
                idxM = idxP
                break
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
                idxM = temp+1
        
        # print(df.loc[idxM,"time"])
        self.Mv = df.loc[idxM,"macd"] # 保存一下本块的MACD极值
        
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
        self.Type = "" #种类

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
    
    #GN04 我们期待dif线已经开始反转
    def CheckGN04(self):
        le = self.RU.Mdif
        ri = self.DF.loc[self.RU.Idx+1, 'dif']
        return abs(le) > abs(ri)

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
        if self.LU.Mdea * self.RU.Mdea < 0 and (self.RU.Idx - self.LU.Idx) < 15:
            return True
        AvgL = (self.LU.Mdea + self.LU.Mdif)/2
        AvgR = (self.RU.Mdea + self.RU.Mdif)/2
        if (AvgR*AvgL)>0 and abs(AvgL)*0.8 > abs(AvgR):
            return True 
        return False

    # 背离的主判断
    def IsDvg(self):
        f_hl = self.F_hl
        RUP = getFixRepClose(f_hl,self.DF,self.RU.Pv)
        if f_hl == 1:  # 高点反转：价格至少接近于新高，同时，MACD减小
            if RUP >= self.LU.Pv*(1 - DvgExtmFixPara) and self.RU.Mv <= self.LU.Mv:
                self.OK = True
                self.Rate = round(self.RU.Mv/self.LU.Mv,3)
        elif f_hl == -1:
            if RUP <= self.LU.Pv*(1 + DvgExtmFixPara) and self.RU.Mv >= self.LU.Mv:
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
class JudgeRst:
    def __init__(self):
        self.Type = "" # 模式 背离 - 通道
        self.F_hl = 0  # 1 顶  -1 底   0 无效
        self.Time = "" # 时间
        self.Mode = "" # 模式
        self.Detail = "" # 详细点位
        self.Patch = "" # 附加检查
    
    def ToPyTime(self):
        FormatDate = "%Y-%m-%d %H:%M:%S"
        if len(self.Time) == 10:
            FormatDate = "%Y-%m-%d"
        self.Time = datetime.datetime.strptime(self.Time, FormatDate)

    # inRst = excel里的记录
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
        return "JudgeRst time:{} type:[{}] flag:{}".format(self.Time,self.Type,self.F_hl)

    def Print(self):
        logger.info(self.String())
        if self.Type != StrChannelSign:
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


#--------------------------------------------全局变量
StrChannelSign = "Channel Sign" # type 通道模式

#--------------------------------------------通道模式

class Channel:
    def __init__(self):  
        pass
    
    def Go(self,df):
        rst = JudgeRst()
        if self.Enter(df) == False:
            return rst
        rst.Type = StrChannelSign # 已经处于通道模式啦
        rst.Time = df.time.iat[-1]
        idxNow = df.index[-1]
        rst.F_hl = IsPriceOutBoll(df,idxNow)
        lrtLimit = 0.2
        lrt = GetLineRate(df,idxNow)
        if (lrt > lrtLimit and rst.F_hl ==1) or  (lrt < lrtLimit*-1 and rst.F_hl == -1):
            print(lrt)
            rst.F_hl = 0
            rst.Type = ""
        return rst

    # 通道模式进入条件检查
    def Enter(self,df):
        br1 = df.borate.iat[-1]
        br2 = df.borate.iat[-2]
        if br1 + br2 < ChanEnter01Para*2:
            return True
        return False
    
    # 手动算boll的rate率
    def GetBollRate(self,df):
        bollgap = df.bup.iat[-1] - df.blow.iat[-1]
        return bollgap/df.blow.iat[-1]

# 判断某的点位的Price是不是在boll轨外
def IsPriceOutBoll(df,idx):
    fg = 0
    fix = 0.02 #万5的缓冲
    open = df.open.at[idx]
    close = df.close.at[idx]
    bup = df.bup.at[idx]*(1-fix/100)
    blow = df.blow.at[idx]*(1+fix/100)
    if open > bup or close > bup:
        fg = 1
    if open < blow or close < blow:
        fg = -1           
    return fg

# 最近7天的斜率
def GetLineRate(df,idx):
    barunit = 3
    bars = 10
    P1 = df.bmid.at[idx]
    P2 = df.bmid.at[idx-bars]
    rst = (P1-P2)/(bars*barunit)
    return rst