
from . import FutuUtil, FutuClass
from . import CBook
import futu as ft
from libs import date


quote_ctx = 1  # 全局的连接上下文

AskL1 = []
BidL1 = []


def Init():
    global quote_ctx
    quote_ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.start()


def InitSZ(SID):
	pass
    # market = ft.Market.SZ
    # ret_code, data = quote_ctx.get_stock_basicinfo(
    #     market, stock_type=ft.SecurityType.STOCK, SID)
    # CheckRetCode(ret_code)
    # FutuUtil.SMap[SID] = data
    # print(SID,data["name"][0])

def InitBasic(SID):
    ret_code, data = quote_ctx.get_stock_basicinfo(
        ft.Market.HK, ft.SecurityType.STOCK, SID)

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
    global AskL1, BidL1
    data = FutuUtil.CleanBookData(data) 

    nb = CBook.Book(data)
    df = nb.ToDF()
    # rstDiff = nb.GetDiff(AskL1, BidL1)
    AskL1 = data["Ask"][:5]
    BidL1 = data["Bid"][:5]
    SID = data["code"]
    print(df)
    # if rstDiff !="":
    #     print(df['core'][0],"diff:",rstDiff)
    # recordData(df, SID)


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
        print("error, msg: %s" % data)
        sys.exit()


def recordData(data, SID):
    stoday = date.SGetTodayMD()
    fPath = 'Docs/csv/' + SID + '_' + stoday + '.csv'
    data.to_csv(fPath, mode='a')
    # FileRW.Afile(fPath, str(data)+"\n")
