
from . import FutuUtil,FutuClass
from . import calc
from futuquant import *
from libs import date


quote_ctx = 1  # 全局的连接上下文


def Init():
    global quote_ctx
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)


def InitBasic(SID):
    ret_code, data = quote_ctx.get_stock_basicinfo(
        Market.HK, SecurityType.STOCK, SID)
    CheckRetCode(ret_code)
    FutuUtil.SMap[SID] = data

def Subs(SID):
    tickHandler = FutuClass.TickerTest(HandleTicker) # 为了回调
    bookhandler = FutuClass.OrderBookTest(HandleBook)
    quote_ctx.set_handler(tickHandler)
    quote_ctx.set_handler(bookhandler)
    quote_ctx.subscribe([SID], [SubType.ORDER_BOOK,SubType.TICKER])

# 回调 摆盘
def HandleBook(data):
    data = FutuUtil.CleanBookData(data)
    SID = data["code"]
    AskL = data['Ask'][0:5]
    BidL = data['Bid'][0:5]
    priceN = calc.GetPriceNow(data)
    s = "%s,%s,%s" % (BidL[0:5][::-1], priceN, AskL[0:5])
    print(s)
    df = pd.DataFrame({'BookList': [s]})
    recordData(df, SID)

# 回调 Ticker
def HandleTicker(data=None):
    SID = data["code"][0]
    data = FutuUtil.CleanTickerData(data)
    # if data["lots"][0] > 5:
    #     print(data)
    print(data)
    recordData(data, SID)

def CheckRetCode(ret_code):
    if ret_code != RET_OK:
        print("error, msg: %s" % data)
        sys.exit()


def recordData(data, SID):
    stoday = date.SGetTodayMD()
    fPath = 'Docs/csv/' + SID +'_'+ stoday + '.csv'
    data.to_csv(fPath, mode='a')
    # FileRW.Afile(fPath, str(data)+"\n")

time.__name__