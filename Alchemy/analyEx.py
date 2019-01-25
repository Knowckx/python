from bookut import extremum,mean
from exut import ex

# 分析极值分布
def extremum1():
    ex.InitSht()
    ex.LoopIdx = 3
    extremum.amplitude = 0.02
    while True:
        str1,i = ex.BookSpeNext(7)
        print("----- 行数",i,str1)
        if str1 == None or str1 == '':
            break
        vv = StrToMean(str1)
        extremum.PutNewV(i,vv)

        if ex.LoopIdx >= 30000:
            break

    extremum.DumpHisty()


def StrToMean(ss):
    strs = ss.split(",")
    for i in range(2):
        strs[i] = float(strs[i])
    me = mean.mean(strs[0],strs[1])
    return me
extremum1()






