# from libs import FileRW
import libs.Win32Excel as ex
import list

p = 0 #最近的new tick
ntCnt = 0 #已经传入多少次tick了
flag = 0 #最近一次的判断
PL3 = [] #3数的数组






# 传入最近的tick
def Core(p):
    Record(p)
    if len(PL3) <2: #刚开始的初始化过程
        initPL3()
        return 0
    rst = dealPL3()
    print('List status：',PL3)
    return rst
    # for p in PL3:
    #     pass

def Record(p1):
    global p,ntCnt
    p = p1
    ntCnt = ntCnt +1
    print('本次的价格为:',p)

def initPL3():
    if len(PL3) == 0:
        PL3.append(p)
        return 0
    elif len(PL3) == 1:
        if PL3[0]==p:
            return 0
        else:
            PL3.append(p)
    print('初始化完成，两个价格为:',PL3)

def dealPL3():
    global flag
    if flag > 9 and p <= min(PL3): #转折信号
        flag = -1
        return flag
    if flag < -9 and p >= max(PL3):
        flag = 1
        return flag
    for pr in PL3:
        if pr == p:  # 新来的价格已经存在
            print('已存在此价格，正常')
            return 0
    if p > max(PL3):
        print('新高')
        if len(PL3)==3:
            list.DelMin(PL3)
        PL3.append(p)
        flag = 10
        return flag
    if p<min(PL3):
        print('新低')
        if len(PL3)==3:
            list.DelMax(PL3)
        PL3.append(p)
        flag = -10
        return flag
    #     pass

def main():
    ex.InitExcelSht()
    func = Core
    ex.LoopCol(func)
    return


main()
