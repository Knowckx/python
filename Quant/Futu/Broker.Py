import time
from futuquant import *

AskL = []
BidL = []
tickL = []

class TickerTest(TickerHandlerBase):
        def on_recv_rsp(self, rsp_str):
                ret_code, data = super(TickerTest,self).on_recv_rsp(rsp_str)
                if ret_code != RET_OK:
                        print("CurKlineTest: error, msg: %s" % data)
                        return RET_ERROR, data
                SeeTicker(data)
                return RET_OK, data

def SeeTicker(data = None):
    tickL = [data['price'][0],data['volume'][0],data['ticker_direction'][0]]
    print(tickL,data.shape[0])


class OrderBookTest(OrderBookHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(OrderBookTest,self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("OrderBookTest: error, msg: %s" % data)
            return RET_ERROR, data
        # print("OrderBookTest ", data) # OrderBookTest自己的处理逻辑
        SeeBookSimple(data)
        return RET_OK, data



def SeeBookSimple(data):
    AskL = data['Ask']
    BidL = data['Bid']
    print("%s,%s,%s" % (BidL[0:3][::-1]," ",AskL[0:3])) 
    
def Print1(tick = None):
    if tick == None:
        print("%s,%s,%s" % (BidL[0:3][::-1]," ",AskL[0:3])) 
        return
    # print("%s,%s,%s" % (BidL[0:3][::-1],tickL[:],AskL[0:3]))
    print("%s" % (BidL))     

StockID = 'HK.08259'
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)


handler1 = TickerTest()
quote_ctx.set_handler(handler1)
quote_ctx.subscribe([StockID], [SubType.TICKER])

handler = OrderBookTest()
quote_ctx.set_handler(handler)
quote_ctx.subscribe([StockID], [SubType.ORDER_BOOK])

