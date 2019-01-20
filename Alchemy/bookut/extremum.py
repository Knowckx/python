

# 判断最大最小值

# amplitude 振幅   波谷到波峰为两倍的振幅。 1倍就可以确定是不是高点低点
amplitude = 0.02
lastL = 0 # 上一次是高点 1 还是低点 -1  init状态 0
maxL = [-1,-1]
minL = [-1,-1]
histyL = []

def PutNewV(nv,idx):
    if maxL[1] == -1: #需要init
        SetMax(nv,idx)  
        SetMin(nv,idx)
        return
    if  nv >= maxL[0]: #new max
        SetMax(nv,idx)
        IsExtm(1)
    elif nv <= minL[0]: #new min
        SetMin(nv,idx)
        IsExtm(-1)

def SetMax(nv,idx):
    maxL[0] = nv
    maxL[1] = idx

def SetMin(nv,idx):
    minL[0] = nv
    minL[1] = idx


#1 new is max | -1 new is min
def IsExtm(mode=1):
    global histyL,lastL
    dif = maxL[0] - minL[0]
    if dif < amplitude:
        return False
    
    # 确定是一个过了gap的极值
    if mode == 1:  #new = maxL[0] 是一个大值
        if lastL == 1 or lastL == 0: # 上一次也是大值 或者上次还没有值。此时可以出极值点
            histyL.append(minL[:])
            lastL = -1  #我们可以断定一个极小值点了
            print("min:",minL)
        SetMin(*maxL)  #最小值回归？ 
    elif mode == -1:
        if lastL == -1 or lastL == 0:
            histyL.append(maxL[:])
            lastL = 1
            print("max:",maxL)
        SetMax(*minL) #未来的新高点一定在本次最低的右边。
    print(minL,maxL,histyL)


def DumpHisty():
    print("DumpHisty:")
    for his in histyL:
        print('%d at %s' % (his[1],his[0]))



# IsExtm(1)