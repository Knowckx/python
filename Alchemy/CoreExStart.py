from exut import ex
from core import core
import sys


#back test in excel.
def Start():
    stdout = sys.stdout
    doc = open('Alchemy\log.txt','w', encoding='utf-8')
    sys.stdout=doc

    tCore = core.Core()
    ex.InitSht()
    # start = 3500
    start = 9700

    # end  = 3700

    end  = 11000
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
    sys.stdout= stdout
    doc.close()


Start()