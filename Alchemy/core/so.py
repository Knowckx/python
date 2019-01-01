# 该盘面的平均手量
def avgLots(bookLL):
    bookL = bookLL[:] #防改
    #10个里，去掉一个最高最低值
    maxl = [-1,-1] # 位置，量
    minl = [-1,9999]
    for i in range(0,len(bookL)):
        tlot = bookL[i][1]
        if tlot > maxl[1]:
            maxl = [i,tlot]
        if tlot < minl[1]:
            minl = [i,tlot]

    if maxl[0] > minl[0]
        bookL.pop(maxl[0])
        bookL.pop(minl[0])
    if maxl[0] < minl[0]
        bookL.pop(minl[0])
        bookL.pop(maxl[0])
    if maxl[0] = minl[0]
        bookL.pop(minl[0])


    difL = bookdiff.Start(bookL[:])
    rst = [0,0]
    f = 0
    for dif in difL[:]:
        p,l = dif[0],dif[1]
        if abs(p) >=11: #先确定系数
            cnt = abs(p) - 11
            f = 1/pow(2,cnt+1)
        else:
            f = 1.2
        vv = f*l #转换过来的数量
        if abs(vv) < 1 :
            continue
        if vv > 0: # 多
            rst[0] = rst[0] + vv
        else: # 空
            rst[1] = rst[1] + abs(vv)
    print('diff:%s ToSign:%s'%(difL[:],rst))
    return rst