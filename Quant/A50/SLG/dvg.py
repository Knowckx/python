import pandas as pd

import Quant.A50.csvdata as csvdata

'''
Divergence   [daɪˈvɜːrdʒəns] 
分歧 背离
'''
# -----------------Main Start-----------------


# -----------------Main End-----------------


# -----------------Func Start-----------------
# func1
def FindNextLeftBlock(macdList, start, minlen):
    i = start
    iLe,iRi = -1,-1
    while i > 0:
        if macdList[i] >= 0:
            i -= 1
            continue
        tempLe = GetLeftofBlock(macdList, i)
        if (i+1-tempLe) >= minlen: # OK
            iLe = tempLe  
            iRi = i+1
            break
        # invalid Block
        i = tempLe - 1
        continue
    return Block(iLe,iRi)

# func1.1 to get the left index of the whole block
def GetLeftofBlock(macdList, right):
    i = right
    while i > 0:
        if macdList[i] < 0:
            i -= 1
            continue
        # > 0
        return i+1
    msg = "GetLeftofBlock Error:Index Out of the Array"
    print(msg)
    return -1

# -----------------Func End-----------------


def GetPointL5(df):
    clList = df['close'][-21:]
    rst = IsLowestL5(clList)
    if rst != "":
        print(rst)
        return


def AnalBlockL5(df):
    mv = df.loc[-1, 'macd']
    if mv > 0:  # MACD is red
        pass
        # return false #TyA
    # MACD is green Synced
    maList = df['macd'][-21:]
    idxL = DigBlock(maList)
    if idxL == -1:
        return
    dfL5 = df[idxL:]
    blockL5 = Block(dfL5)
    blockL5.Anal()


# P2.1 值和M值是同步的
def IsPointSyncPM(MV):
    if MV > 0:  # MACD is red
        return false
    return true


# P1 长21的close数组
def IsLowestL5(clList):
    low21 = clList.idxmin()
    if low21 == -1:  # P1 OK
        return ""
    msg = "close[-1] is not lowest"
    return msg


#　obj represent macd Block 
class Block:
    def __init__(self):
        self.ILe = 0
        self.IRi = 0

    def __init__(self,left,right):
        self.ILe = left
        self.IRi = right

    def Anal(self, df):
        self.Len = len(self.df)
        idxp = df.close.idxmin()
        idxm = df.macd.idxmin()
        if idxp == idxm:
            self.dvgUt = DvgUnit(df, idxp)
            msg = "Block Desc:Single"
            print(msg)
            return
        # Try TyB
        idxL, idxR = idxm, idxp
        if idxL > idxR:
            idxL, idxR = idxR, idxL
        dvgSet = DvgSet(df, idxL, idxR)
        self.TypeB = devSet.IsDvg()
        return


# dvg 对比单位
class DvgUnit:
    def __init__(self):
        self.Idx = 0
        self.Pv = 0.0
        self.Mv = 0.0

    def __init__(self, df, idx):
        self.Idx = idx
        self.Pv = df.loc[idx, 'close']
        self.Mv = df.loc[idx, 'macd']


class DvgSet:
    def __init__(self):
        self.LU = DvgUnit()
        self.RU = DvgUnit()

    def __init__(self, df, idxL, idxR):
        self.LU = DvgUnit(df, idxL)
        self.RU = DvgUnit(df, idxR)

    def IsDvg(self):
        if RU.Pv <= LU.Pv and Ru.Mv >= LU.Pv:
            return True
        return False
