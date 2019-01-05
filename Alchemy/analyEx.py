from bookut import extremum
from exut import ex

# 分析整个极值分布
def extremum1():
    ex.InitSht()
    ex.LoopIdx = 3
    while True:
        bookL,i = ex.BookNext()
        if len(bookL) == 0:
            return
        print("----- 行数",i)
        ActionSetMean(bookL,i)

def ActionSetMean(book,i):
    rst = mean.GetPredictP(book)
    ex.SetCell(i,7,rst)

extremum1()
    sht = ex.InitExcelSht()
    coreCol = 7
    i = 0






