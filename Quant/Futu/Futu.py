import futu as ft




def Init():
    pass

#ID 'HK.00700'
def GetTick(ID):
    quote_ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx.subscribe([ID], [SubType.TICKER])
    ok,dfData = quote_ctx.get_rt_ticker(ID, 1000)
    if ok == RET_OK: # RET_OK是他的全局变量哦
        return dfData
    quote_ctx.close()

def GetTickToExcel(StockID):
    df = GetTick(StockID)
    fPath = 'Docs/' + StockID + '.xlsx'
    # df.to_excel('tmp.xlsx',sheet_name=StockID)
    df.to_excel(fPath,sheet_name=StockID)

StockID = 'HK.08259'
GetTickToExcel(StockID)