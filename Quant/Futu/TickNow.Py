import time
from FutuLib import FutuUtil, FutuFunc
import futu as ft


import futu as ft
from libs import FileRW

def StartStockTick():
    # SID = 'SZ.000776' 
    SID = 'HK.00700'  

    FutuFunc.InitBasic(SID)
    FutuFunc.Subs(SID)

def Main():
    FutuFunc.Init()
    StartStockTick()


Main()
