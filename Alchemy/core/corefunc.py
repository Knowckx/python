# 放core相关的函数

from Alchemy.bookut import bookdiff

# 返回 转化为[+-11]上的相对变动
# 
def difToSignal(bookL):
    difL = bookdiff.Start(bookL[:])
    rst = [0,0]
    f = 0
    for dif in difL[:]:
        p,l = dif[0],dif[1]
        if abs(p) >11: #先确定系数
            cnt = abs(p) - 11
            f = 1/pow(2,cnt+1)
        else:
            f = 1
        vv = f*l #转换过来的数量
        if abs(vv) < 1 :
            continue
        if vv > 0: # 多
            rst[0] = rst[0] + vv
        else: # 空
            rst[1] = rst[1] + abs(vv)
    if isZero(rst):
        return None
    if rst[0] == rst[1]: #[-11, -26], [11, 26] 这种情况，是多空同时增量力量
        rst = [c/10 for c in rst]
        
    # print('diff:%s ToDifSign:%s'%(difL[:],rst))
    return rst

def isZero(dif):
    if dif[0]==0 and dif[1]==0:
        # print("dif is %s.Pass"%dif)
        return True
    return False