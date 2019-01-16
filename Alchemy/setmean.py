from exut import ex
from bookut import mean
from bookut import extremum


# 期望值
def setmean():
    ex.InitSht()
    ex.LoopIdx = 2500
    endIdx = 3000
    while True:
        bookL,i = ex.BookNext()
        if len(bookL) == 0:
            break
        if i >= endIdx:
            break
        print("----- 行数",i)
        Action(bookL,i)

def Action(book,i):
    rst = mean.GetPredictP(book)
    ss = rst.String()
    ex.SetCell(i,7,ss)
    # vv = sht.Cells(i, coreCol).Value


setmean()






