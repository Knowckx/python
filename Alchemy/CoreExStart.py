from exut import ex
from core import core



#back test in excel.
def Start():
    tCore = core.Core()
    ex.InitSht()
    # start = 3500
    start = 4300

    # end  = 3700

    end  = 4680
    ex.LoopIdx = start #dubug start
    # ex.LoopIdx = 20522 #dubug
    # ex.LoopIdx = 20658 #dubug


    while True:
        bookL,i = ex.BookNext()
        if i >= end:
            break
        if len(bookL) == 0:
            return
        print("----- 行数",i)
        tCore.PutNew(bookL,i)

    tCore.DumpHisty()

Start()