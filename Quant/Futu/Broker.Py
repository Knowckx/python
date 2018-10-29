import time
from futuquant import *

class OrderBookTest(OrderBookHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(OrderBookTest,self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("OrderBookTest: error, msg: %s" % data)
            return RET_ERROR, data

        print("OrderBookTest ", data) # OrderBookTest自己的处理逻辑

        return RET_OK, data

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
handler = OrderBookTest()
quote_ctx.set_handler(handler)

StockID = 'HK.01034'
quote_ctx.subscribe([StockID], [SubType.BROKER])
# time.sleep(15)
# quote_ctx.close()




