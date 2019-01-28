
from futu import *


class TickerTest(TickerHandlerBase):
    def __init__(self, HandlerFunc):
        self.HandlerFunc = HandlerFunc

    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(TickerTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("CurKlineTest: error, msg: %s" % data)
            return RET_ERROR, data
        self.HandlerFunc(data)
        return RET_OK, data


class OrderBookTest(OrderBookHandlerBase):
    def __init__(self, HandlerFunc):
        self.HandlerFunc = HandlerFunc

    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(OrderBookTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("OrderBookTest: error, msg: %s" % data)
            return RET_ERROR, data
        self.HandlerFunc(data)
        return RET_OK, data
