


# 去掉最大最小值后的平均lots
def AvgLotL(bookLL):
    ll = CleanLotL(bookLL[:])
    cnt,tt = 0,0
    for l in ll[:]:
        if l != 0:
            cnt = cnt + 1
            tt = tt+ l
    avg = tt/cnt
    return avg

# 去掉最大最小值后的lots
def CleanLotL(bookLL):
    lotL = []
    for b in bookLL[0]:
        lotL.append(b[1])
    for b in bookLL[1]:
        lotL.append(b[1])
    DelMin(lotL)
    DelMax(lotL)
    return lotL





def DelMin(li):
    li.pop(li.index(min(li)))


def DelMax(li):
    li.pop(li.index(max(li)))



# 遍历转类型
def TupleToList(tu):
    rst = []
    for t in tu:
        rst.append(t)
    return rst