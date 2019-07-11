import pandas as pd

from .c_dvg import *

'''
Divergence [daɪˈvɜːrdʒəns] 
分歧 背离
'''

#experience args
ExtmCheckLen = 20


# -----------------Main Start-----------------
def Start(df):
    print(df[-5:])
    
    # pre is lowest or highest
    rst = IsExtmAndTurn(df.close)
    return 
    bokl5 = GetBlockL5(df) 
    idxNow = bokl5.ILe
    if idxNow == -1:
        return
    mali = df.macd
    limit = bokl5.Len()*0.75
    bokl10 = FindNextLeftBlock(mali,idxNow,limit)
    bokl10.Anal()

    mSet = DvgSet(df,bokl10.IRep,bokl5.IRep)
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
        return -1
    idxhigh = closeList.idxmax()
    if idxhigh == idxTar:
        return 1
    return 0
# -----------------P0 pre End-----------------



# -----------------P1 Start-----------------

def GetBlockL5():
    clList = df['close'][-21:]
    rst = IsLowestL5(clList)
    if rst != "":
        print(rst)
        return
    return Block(50,60)



# -----------------P1 End-----------------



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
