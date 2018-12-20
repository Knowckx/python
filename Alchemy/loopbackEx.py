from exut import ex
from core import core



#back test in excel.
def Start():
    ex.InitSht()
    while True:
        bookL = ex.BookNext()
        if len(bookL) == 0:
            return
        print(bookL)
        core.Core(bookL)

Start()