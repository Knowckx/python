from exut import ex
from core import core



#back test in excel.
def Start():
    tCore = core.Core()
    ex.InitSht()
    # ex.LoopIdx = 20480 #dubug start
    # ex.LoopIdx = 20522 #dubug
    ex.LoopIdx = 20658 #dubug


    while True:
        bookL,i = ex.BookNext()
        if len(bookL) == 0:
            return
        print("----- 行数",i)
        tCore.PutNew(bookL)

Start()