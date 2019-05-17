import time
from FutuLib import FutuUtil, FutuFunc
import futu as ft


import futu as ft
from libs import FileRW

def StartStockTick():
    # StockID = 'SZ.002376'  
    SID = 'SH.601339'  
    FutuFunc.InitBasic(SID)
    FutuFunc.Subs(SID)

def Main():
    FutuFunc.Init()
    StartStockTick()


Main()
