import time
from futuquant import *
from libs import FileRW

info = {}

class TickerTest(TickerHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(TickerTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("CurKlineTest: error, msg: %s" % data)
            return RET_ERROR, data
        HandleTicker(data)
        return RET_OK, data


class OrderBookTest(OrderBookHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(OrderBookTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("OrderBookTest: error, msg: %s" % data)
            return RET_ERROR, data
        # print("OrderBookTest ", data) # OrderBookTest自己的处理逻辑
        HandleBook(data)
        return RET_OK, data


def HandleTicker(data=None):
    SID = data["code"][0]
    data = data[['price', 'volume', 'ticker_direction', 'time']]
    df = data.rename(columns={'ticker_direction': 'type'})
    print(df)
    recordData(df, SID)
    # tickL = [data['time'][0],data['price'][0],data['volume'][0],data['ticker_direction'][0]]
    # print(tickL,data.shape[0])


def HandleBook(data):
    SID = data["code"]
    AskL = data['Ask'][0:5]
    BidL = data['Bid'][0:5]
    priceN = GetPriceNow(data)
    s = "%s,%s,%s" % (BidL[0:3][::-1], priceN, AskL[0:3])
    print(s)
    df=pd.DataFrame({ 'BookList': [s] })
    recordData(df, SID)


def GetPriceNow(bookN):
    AskL = bookN['Ask']
    BidL = bookN['Bid']
    P0 = GetBan(AskL[0],BidL[0])
    P1 = GetBan(AskL[0],BidL[0])
    P2 = GetBan(AskL[0],BidL[0])
    if P1 == -1:
        P1 = P0
    if P2 == -1:
        P2 = P0
    rst = 0.75*P0 + 0.15*P1 + 0.1*P2
    rst = round(rst, 5)
    return rst

def GetBan(B0,S0):
    tvo = B0[1]+S0[1]
    if tvo == 0:
        return -1
    p = (S0[1]/tvo*B0[0])+(B0[1]/tvo*S0[0])
    return p

def recordData(data, SID):
    fPath = 'Docs/csv/' + SID + '.csv'
    data.to_csv(fPath, mode='a')

    # FileRW.Afile(fPath, str(data)+"\n")


def recordData1(data, SID):
    fPath = 'Docs/' + SID + '.txt'
    FileRW.Afile(fPath, str(data)+"\n")


def StartStock(quote_ctx, SID):
    print(quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK, SID))
    bi = quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK, SID)
    # info['SID'] = bi['lot_size'][0]
    handler0 = TickerTest()
    quote_ctx.set_handler(handler0)
    quote_ctx.subscribe([SID], [SubType.TICKER])
    handler1 = OrderBookTest()
    quote_ctx.set_handler(handler1)
    quote_ctx.subscribe([SID], [SubType.ORDER_BOOK])


def Main():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    StockID = 'HK.02258'
    StartStock(quote_ctx, StockID)
    StockID = 'HK.06890'
    StartStock(quote_ctx, StockID)


Main()
