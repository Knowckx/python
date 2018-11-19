

SMap = {}  # 关于股票的基础信息

def GetLotSize(SID):
    info = SMap[SID]
    lotsize = info["lot_size"][0]
    return lotsize




# 清理一下Book的数据，主要是volum转lots
def CleanBookData(BookMap):
    SID = BookMap["code"]
    size = GetLotSize(SID)
    BookMap['Ask'] = LotSizeinList(BookMap['Ask'],size)
    BookMap['Bid'] = LotSizeinList(BookMap['Bid'],size)
    return BookMap
    # print(BookMap)
    # 结构： BookMap['Ask'] = list     list = [(1.02, 148000, 20),.....]   (1.02, 148000, 20) = tuple

def LotSizeinList(orders,size):
    outs = []
    for order in orders:  # [(1.02, 148000, 20),.....]
        out = list(order)
        out[1] = int(out[1]/size)
        out.pop()   # 最后一项目前订单数量不要了
        outs.append(out)
    return outs


def CleanTickerData(data):
    SID = data["code"][0]
    size = GetLotSize(SID)
    data['volume'] = data['volume'].map(lambda x: int(x/size))

    # print(type(data['time'][0])) #这个时间的处理

    data = data[['price', 'volume', 'ticker_direction', 'time']]
    data = data.rename(columns={'ticker_direction': 'type','volume': 'lots'})

    return data