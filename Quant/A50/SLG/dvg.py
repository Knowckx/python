import pandas as pd

from .c_dvg import *

'''
Divergence [daɪˈvɜːrdʒəns] 
分歧 背离
'''

# experience args
ExtmCheckLen = 20  #20天差不多了，上涨中的回调产生的背离大概间隔20天


# -----------------Main Start-----------------
def Start(df):
    # pre is lowest or highest
    rst = IsExtmAndTurn(df.close)
    if rst.F_hl == 0:
        # print("IsExtmAndTurn false,continue")
        return -1
    print("IsExtmAndTurn In -->", df.loc[df.index[-1], 'time'])
    dvg = DvgSet(df,rst.f_hl)
    dvg.Go()
    return 

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
