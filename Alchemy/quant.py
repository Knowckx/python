# coding: utf-8

##### 下方代码为 IDE 运行必备代码 #####
if __name__ == '__main__':
    import jqsdk
    params = {
        'token': '9ed36770e86d78ad7fccd4ab608238d2',
        'algorithmId': 2,
        'baseCapital': 1000000,
        'frequency': 'day',
        'startTime': '2017-06-01',
        'endTime': '2017-08-01',
        'name': "Test1",
    }
    jqsdk.run(params)

##### 下面是策略代码编辑部分 #####

from jqdata import *

def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    log.info('initialize run only once')
    run_daily(market_open, time='open', reference_security='000300.XSHG')


def market_open(context):
    # 输出开盘时间
    log.info('(market_open):' + str(context.current_dt.time()))

