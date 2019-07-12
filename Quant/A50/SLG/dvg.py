import pandas as pd

from .c_dvg import *

'''
Divergence [daɪˈvɜːrdʒəns] 
分歧 背离
'''

# experience args
ExtmCheckLen = 20
RecnetBarsLen = 100


# -----------------Main Start-----------------
def Start(df):
    print(df[-5:])

    # pre is lowest or highest
    rst = IsExtmAndTurn(df.close)
    if rst.F_hl == 0:
        print("IsExtmAndTurn return false,continue")
        return
    # P1 dig Block L5
    dfRecent = df[-RecnetBarsLen:]
    bokl5 = GetBlockL5(dfRecent, rst)
    # P2 dig Block L10
    l10args = SearchBlockL10Args(bokl5.ILe-1, rst.F_hl, bokl5.Len())

    bokL10 = GetBlockL10(df, l10args)
    if bokL10.ILe == -1:
        print("find bokL10 failed,continue")
        return

    # P3 two Block Anal
    mSet = DvgSet(df, bokl10.RepUn, bokl5.RepUn)
    rst = mSet.IsDvg()
    print(rst)


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
    bokl5 = DigBlock(df.macd, extmRst.Idx, extmRst.F_hl)
    bokl5.Anal()
    return bokl5

# -----------------P1 End-----------------

# -----------------P2 Start-----------------

# 给出符合长度的block


def GetBlockL10(df, args):
    idxNow = args.IdxNow
    maxTry = 3  # 参见2018-06出现的间杂点
    while maxTry > 0:
        tempBok = FindNextBlock(df.close, idxNow, args.F_hl)
        if tempBok.Len() <= args.MinLen:
            idxNow = tempBok.ILe-1
            maxTry -= 1
            continue
        # success
        BokL10 = tempBok
        BokL10.Anal(df)
        return BokL10
    return Block()

    # -----------------P2 End-----------------

    # -----------------Func Start-----------------
    # func1

# 返回下一个block


def FindNextBlock(macdList, start, f_hl):
    iri = GetNextBlockStart(macdList, start, f_hl)
    tempBok = DigBlock(macdList, idxRt, h_l)
    return tempBok

# return the


def GetNextBlockStart(macdList, start, f_hl):
    i = start
    while i > 0:
        if (macdList[i] >0 and f_hl == 1) or (macdList[i] < 0 and f_hl == -1)
        
            i -= 1
            continue


# func1 given index_right,given ask [high,1,red or low,-1,green] to find the wholeblock
# return the block with [left , right]
def DigBlock(macdList, idxRt, h_l):
    bokl5 = Block()
    # check Block is point style
    mv = macdList[idxRt]
    if (isred and mv < 0) or ((not isred) and mv > 0):
        bokl5.ILe = idxRt
        bokl5.IRi = idxRt
        bokl5.RepUn = DvgUnit(df, idxRt)
        print("Broker is a point")
        return bokl5

    # common Block. get the left of block
    ife = GetBlockLeft(macdList, idxRt, h_l)


# func1.1 to get the left index of the whole block
def GetBlockLeft(macdList, right, h_l):
    i = right
    while i > 0:
        if macdList[i] < 0:
            i -= 1
            continue
        # > 0
        return i+1
    msg = "GetLeftofBlock1 Error:Index Out of the Array"
    print(msg)
    return -1

# -----------------Func End-----------------
