import time
from FutuLib import FutuUtil, FutuFunc
from futuquant import *
from libs import FileRW

def StartStockTick(SID):
    # quote_ctx = FutuFunc.quote_ctx
    # 基础信息
    FutuFunc.InitBasic(SID)
    FutuFunc.Subs(SID)


def Main():
    FutuFunc.Init()
    StockID = 'HK.01119'  #达力环保

    StartStockTick(StockID)


Main()
