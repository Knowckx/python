
from . import FutuUtil, FutuClass
from . import CBook
import futu as ft
from libs import date
from Alchemy.core import c_TI_BA


quote_ctx = 1  # 全局的连接上下文

SignBA = c_TI_BA.TIBA(20)



def Init():
    global quote_ctx
    quote_ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.start()


def InitBasic(SID,flag = "HK"):
    market = ft.Market.HK
    if flag == "SZ":
        flag = ft.Market.SZ
    ret_code, data = quote_ctx.get_stock_basicinfo(market, ft.SecurityType.STOCK, SID)
    CheckRetCode(ret_code)
    FutuUtil.SMap[SID] = data
    print(SID, data["name"][0])


def Subs(SID):
    tickHandler = FutuClass.TickerTest(HandleTicker)  # 为了回调
    quote_ctx.set_handler(tickHandler)
    bookhandler = FutuClass.OrderBookTest(HandleBook)
    quote_ctx.set_handler(bookhandler)
    quote_ctx.subscribe([SID], [ft.SubType.ORDER_BOOK, ft.SubType.TICKER])


# 回调 摆盘
def HandleBook(data):
    data = FutuUtil.CleanBookData(data) 
    nb = CBook.Book(data)
    DifL = nb.GetDiff()
    if DifL == None:
        return
    df = nb.ToDF()
    print(df)
    print('Ticket Dif:%s'%(DifL))
    SignBA.Add(DifL)
    SignBA.Print()


# 回调 Ticker
def HandleTicker(data=None):
	pass
    # SID = data["code"][0]
    # data = FutuUtil.CleanTickerData(data)
    # if data["lots"][0] > 5:
    #     print(data)
#     print(data)
    # recordData(data, SID)


def CheckRetCode(ret_code):
    if ret_code != ft.RET_OK:
        print("error, msg: %s" % ret_code)


def recordData(data, SID):
    stoday = date.SGetTodayMD()
    fPath = 'Docs/csv/' + SID + '_' + stoday + '.csv'
    data.to_csv(fPath, mode='a')
    # FileRW.Afile(fPath, str(data)+"\n")
