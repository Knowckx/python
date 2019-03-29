import time
from FutuLib import FutuUtil, FutuFunc
import futu as ft


import futu as ft
from libs import FileRW

def StartStockTick(SID):
    # quote_ctx = FutuFunc.quote_ctx
    # 基础信息
    FutuFunc.InitBasic(SID)
    # FutuFunc.InitSZ(SID)

    
    FutuFunc.Subs(SID)



def Main():
    FutuFunc.Init()

    StockID = 'HK.14221'  #MET
    # StockID = 'SZ.002183'  #MET


    StartStockTick(StockID)


Main()
