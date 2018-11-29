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
    # StockID = 'HK.02258'
    # StartStock(quote_ctx, StockID)
    # StockID = 'HK.06890'  #康利国际
    # StockID = 'HK.01761'  #宝宝树
    StockID = 'HK.01790'  #达力环保

    StartStockTick(StockID)


Main()
