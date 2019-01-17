from bookut import extremum,mean
from exut import ex

# 分析极值分布
def extremum1():
    ex.InitSht()
    ex.LoopIdx = 3500
    extremum.amplitude = 0.01
    while True:
        str1,i = ex.BookSpeNext(7)
        if str1 == None or str1 == '':
            return
        print("----- 行数",i)
        vv = StrToMean(str1)
        extremum.PutNewV(vv,i)

        if ex.LoopIdx >= 4682:
            break
    extremum.DumpHisty()

def StrToMean(ss):
    strs = ss.split(",")
    for i in range(2):
        strs[i] = float(strs[i])
    me = mean.mean(strs[0],strs[1])
    return me
extremum1()






