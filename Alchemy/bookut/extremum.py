

# 判断最大最小值

# amplitude 振幅   波谷到波峰为两倍的振幅。 1倍就可以确定是不是高点低点
amplitude = 0.02
lastL = [-2,-2] # 还没有出现第一次极值  (v, -1 | +1)
maxL = [-1,-1]
minL = [-1,-1]
histyL = []


def SetLast(nv,idx):
    lastL[0] = nv
    lastL[1] = idx

def SetMax(nv,idx):
    maxL[0] = nv
    maxL[1] = idx

def SetMin(nv,idx):
    minL[0] = nv
    minL[1] = idx

def PutNewV(nv,idx):
    if maxL[1] == -1:
        SetMax(nv,idx)  #init
        SetMin(nv,idx)
        return
    if  minL[0] < nv < maxL[0]:  #mid
        return
    elif nv > maxL[0]: #new max
        SetMax(nv,idx)
        IsExtm(1)
    elif nv < minL[0]: #new min
        SetMin(nv,idx)
        IsExtm(-1)

#1 new is max | -1 new is min
def IsExtm(mode=1):
    global histyL
    dif = maxL[0] - minL[0]
    if dif < amplitude:
        return False
    
    # 确定是一个极值
    if mode == 1:
        if lastL[1] != -1:
            SetLast(minL[0],-1)
            histyL.append(minL[:])
            print("min:",minL)
        SetMin(*maxL)  #最小值回归？ 
    elif mode == -1:
        if lastL[1] != 1:
            SetLast(maxL[0],1)
            histyL.append(maxL[:])
            print("max:",maxL)
        SetMax(*minL)
    print(minL,maxL,histyL)


def DumpHisty():
    print("DumpHisty:")
    for his in histyL:
        print(his)



# IsExtm(1)