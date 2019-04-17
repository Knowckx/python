import time
from FutuLib import FutuUtil, FutuFunc
import futu as ft


import futu as ft
from libs import FileRW

def StartStockTick():
    # StockID = 'SZ.002376'  
    SID = 'SZ.002376'  
    FutuFunc.InitBasic(SID)
    FutuFunc.Subs(SID)

def Main():
    FutuFunc.Init()
    StartStockTick()


Main()
