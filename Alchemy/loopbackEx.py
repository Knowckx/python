from exut import ex
from core import core



#back test in excel.
def Start():
    tCore = core.Core()
    ex.InitSht()
    ex.LoopIdx = 20489 #dubug

    while True:
        bookL,i = ex.BookNext()
        if len(bookL) == 0:
            return
        print("----- 行数",i)
        tCore.PutNew(bookL)

Start()