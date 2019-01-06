from bookut import extremum
from exut import ex

# 分析极值分布
def extremum1():
    ex.InitSht()
    ex.LoopIdx = 3500
    extremum.amplitude = 0.01
    while True:
        vv,i = ex.BookSpeNext(7)
        if vv == None or vv == '':
            return
        print("----- 行数",i)
        extremum.PutNewV(vv,i)

        if ex.LoopIdx >= 4682:
            break
    extremum.DumpHisty()
extremum1()






