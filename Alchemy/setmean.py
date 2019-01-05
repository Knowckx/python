from exut import ex
from bookut import mean
from bookut import extremum


# 期望值
def setmean():
    ex.InitSht()
    ex.LoopIdx = 3
    while True:
        bookL,i = ex.BookNext()
        if len(bookL) == 0:
            break
        print("----- 行数",i)
        Action(bookL,i)
    extremum.DumpHisty()

def Action(book,i):
    rst = mean.GetPredictP(book)
    # ex.SetCell(i,7,rst)

    # vv = sht.Cells(i, coreCol).Value
    vv = rst
    extremum.PutNewV(vv,i)

setmean()



