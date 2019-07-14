import pandas as pd

from .c_dvg import *

'''
Divergence [daɪˈvɜːrdʒəns] 
分歧 背离
'''

# experience args
ExtmCheckLen = 20  #20天差不多了，上涨中的回调产生的背离大概间隔20天
RecnetBarsLen = 100


# -----------------Main Start-----------------
def Start(df):
    # pre is lowest or highest
    rst = IsExtmAndTurn(df.close)
    if rst.F_hl == 0:
        # print("IsExtmAndTurn false,continue")
        return -1
    print("IsExtmAndTurn In -->", df.loc[df.index[-1], 'time'])
    # P1 dig Block L5
    dfRecent = df[-RecnetBarsLen:]
    bokL5 = GetBlockL5(dfRecent, rst)
    # P2 dig Block L10
    NewStart = bokL5.ILe-1
    l10df = df.loc[:NewStart]
    # print(l10df[-5:])
    l10args = SearchBlockL10Args(NewStart, rst.F_hl, bokL5.Len())
    bokL10 = GetBlockL10(l10df, l10args)

    # P3 two Block Anal
    idxNext = FinalLog(bokL5,bokL10)
    return idxNext
   

# -----------------Main End-----------------

# -----------------pre Start-----------------

# price now is extremum and turn  va -1 lowest 1 hight 0 normal
def IsExtmAndTurn(clList):
    closeList = clList[-ExtmCheckLen:]
    idxTar = closeList.index[-2]
    idxlow = closeList.idxmin()
    if idxlow == idxTar:
        return ExtmCheckRst(-1, idxlow)
    idxhigh = closeList.idxmax()
    if idxhigh == idxTar:
        return ExtmCheckRst(1, idxhigh)
    return ExtmCheckRst(0, -1)
# -----------------pre End-----------------

# -----------------P1 Start-----------------
def GetBlockL5(df, extmRst):
    bokL5 = DigBlock(df, extmRst.Idx, extmRst.F_hl)
    bokL5.Anal()
    return bokL5

# -----------------P1 End-----------------

# -----------------P2 Start-----------------

# 给出符合长度的block
def GetBlockL10(df, args):
    idxNow = args.IdxNow
    maxTry = 3  # 参见2018-06出现的间杂点
    maxBars = 40 # 向前寻找最多2个月*20天
    while maxTry > 0 and maxBars > 0:
        tempRi = GetNextBlockStart(df.macd, idxNow,args.F_hl) #1
        maxBars -= (idxNow - tempRi)
        if maxBars < 0:
            break 

        tempBok = DigBlock(df, tempRi, args.F_hl) #2
        # tempBok = FindNextBlock(df, idxNow, args.F_hl)
        if tempBok.Len() <= args.MinLen:
            maxTry -= 1
            maxBars -= tempBok.Len()
            idxNow = tempBok.ILe-1
            continue
        # success
        BokL10 = tempBok
        BokL10.Anal()
        return BokL10
    return Block()

    # -----------------P2 End-----------------

    # -----------------Func Start-----------------
    # func1

# 返回下一个block


# def FindNextBlock(df, start, f_hl):
#     iri = GetNextBlockStart(df.macd, start, f_hl)
#     tempBok = DigBlock(df, iri, f_hl)
#     return tempBok

# return the


def GetNextBlockStart(macdList, start, f_hl):
    i = start
    while i > 0:
        if (f_hl == 1 and macdList[i] >0) or (f_hl == -1 and macdList[i] < 0):
            # get the right [x,right]
            return i
        i -= 1


# func1 given index_right,given ask [high,1,red or low,-1,green] to find the wholeblock
# return the block with [left , right]
def DigBlock(df, idxRt, h_l):
    macdList = df.macd
    bokL5 = Block()
    # check Block is point style
    mv = macdList[idxRt]
    if (h_l == 1 and mv < 0) or (h_l == -1 and mv > 0):
        bokL5.Init(idxRt,idxRt,h_l,df)
        # bokL5.RepUn = DvgUnit().Init(df, idxRt)
        print("Broker is a point")
        return bokL5
    # common Block. get the left of block
    ift = GetBlockLeft(macdList, idxRt, h_l)
    if ift == -1:
        return bokL5
    bokL5.Init(ift,idxRt,h_l,df)
    return bokL5


# func1.1 to get the x of [x,right]
def GetBlockLeft(macdList, right, h_l):
    i = right
    while i > 0:
        if (h_l < 0 and  macdList[i] < 0) or (h_l > 0 and  macdList[i] > 0):
            i -= 1
            continue
        # > 0
        return i+1
    msg = "GetLeftofBlock1 Error:Index Out of the Array"
    print(msg)
    return -1

# -----------------Func End-----------------


# -----------------P3 Log Result-----------------
def FinalLog(bokL5,bokL10):
    nextStart = -1
    mod = ""
    print("Anal result:")
    if bokL5.TyB:
        print("find L5 TypeB Dvg")
        bokL5.TyB_Set.Print()  
        nextStart = bokL5.ILe
        mod = "1.1"

    if bokL10.ILe != -1:
        mSet = DvgSet()
        mSet.InitBlock2(bokL10.RepUn, bokL5.RepUn, bokL5.F_hl)
        rst = mSet.IsDvg()
        if rst:
            print("find Block Dvg")
            mSet.Print()
            mod = "2.0" + mod
            nextStart = bokL5.ILe
    if mod == "":
        print("<--- None Out")
    else :
        print("<--- Success")
    return  nextStart
    

# -----------------P3 End-----------------