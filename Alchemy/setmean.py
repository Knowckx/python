from exut import ex
from bookut import mean
from bookut import extremum


last = 0

# 期望值
def setmean():
    ex.InitSht()
    ex.LoopIdx = 10685
    endIdx = 10736
    while True:
        bookL,i = ex.BookNext()
        if len(bookL) == 0:
            break
        if i >= endIdx:
            break
        print("----- 行数",i)
        Action(bookL,i)

def Action(book,i):
    global last
    rst = mean.GetPredictP(book)
    print(rst-last)
    last = rst
    # ss = rst.String()
    # ex.SetCell(i,7,ss)
    # vv = sht.Cells(i, coreCol).Value

    #研究下724 726
setmean()
# 10692 0.6859540864598352 大
# 10728 0.6859263581721345 小





