from futuquant import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
quote_ctx.subscribe(['HK.08611'], [SubType.TICKER])
print(quote_ctx.get_rt_ticker('HK.08611', 10))
quote_ctx.close()