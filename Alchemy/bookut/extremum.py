

# 判断最大最小值

# amplitude 振幅   波谷到波峰为两倍的振幅。 1倍就可以确定是不是高点低点
amplitude = 0.02
lastL = 0 # 上一次是高点 1 还是低点 -1  init状态 0
maxL = [-1,-1]
minL = [-1,-1]
histyL = []

def PutNewV(idx,nv):
    if maxL[0] == -1: #需要init
        SetMax(idx,nv)  
        SetMin(idx,nv)
        return
    if  nv >= maxL[1]: #new max
        SetMax(idx,nv)
        IsExtm(1)
    elif nv <= minL[1]: #new min
        SetMin(idx,nv)
        IsExtm(-1)

def SetMax(idx,nv):
    maxL[0] = idx
    maxL[1] = nv


def SetMin(idx,nv):
    minL[0] = idx
    minL[1] = nv


#1 new is max | -1 new is min
def IsExtm(mode=1):
    global histyL,lastL
    dif = maxL[1] - minL[1]
    if dif < amplitude:
        return False
    
    # 确定是一个过了gap的极值
    if mode == 1:  #new = maxL[0] 是一个大值
        if lastL == 1 or lastL == 0: # 上一次也是大值 或者上次还没有值。此时可以出极值点
            addHis(minL[:])
            lastL = -1  #我们可以断定一个极小值点了
            print("min:",minL)
        SetMin(*maxL)  #最小值回归？ 
    elif mode == -1:
        if lastL == -1 or lastL == 0:
            addHis(maxL[:])
            lastL = 1
            print("max:",maxL)
        SetMax(*minL) #未来的新高点一定在本次最低的右边。
    # print(minL,maxL,histyL)



def addHis(Li):
    global histyL
    # L = utlist.TupleToList(Li)
    L = Li
    hisL = histyL
    if len(hisL) > 0:
        last = hisL[-1] #上一次的极点
        dif = GetDifPst(last[1],L[1]) #
        last.append(dif)
    histyL.append(L)

# 两数差值的百分比
def GetDifPst(v1,v2):
    dw = v1.V()
    dif = (v2 - v1)/dw*100
    return round(dif,2)

    
def DumpHisty():
    global histyL
    print("DumpHisty:")
    for his in histyL:
        ss = '%d : %s' % (his[0],his[1])
        if len(his) == 3:
            ss= '%s,%s%%' % (ss,his[2])
        print(ss)




# IsExtm(1)