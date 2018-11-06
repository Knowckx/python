import time
from futuquant import *

class TickerTest(TickerHandlerBase):
        def on_recv_rsp(self, rsp_str):
                ret_code, data = super(TickerTest,self).on_recv_rsp(rsp_str)
                if ret_code != RET_OK:
                        print("CurKlineTest: error, msg: %s" % data)
                        return RET_ERROR, data

                print("TickerTest ", data) # TickerTest自己的处理逻辑
                return RET_OK, data

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
handler = TickerTest()
quote_ctx.set_handler(handler)

StockID = 'HK.08259'
quote_ctx.subscribe([StockID], [SubType.TICKER])
# time.sleep(100)
# quote_ctx.close()




