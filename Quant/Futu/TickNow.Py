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
    # StockID = 'HK.00700'  #国际
    # StockID = 'HK.03992'  #创毅
    # StockID = 'HK.02798'  #久泰邦达
    StockID = 'HK.08622'  #MET

    StartStockTick(StockID)


Main()
