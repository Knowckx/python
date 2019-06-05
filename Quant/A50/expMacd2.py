# 导入函数库
import libut


# ('002624.XSHE', '60m') ??
# 初始化函数，设定基准等等
def initialize(context):
    # stocks = libut.GetAllSts()
    stocks = get_concept_stocks('GN780', date='2019-05-21')
    # stocks = [normalize_code('300003')]
    print("total stocks",len(stocks))
    for st in stocks:
        F_MACD_TypeA_in(st)
    # print(ok)

def F_MACD_TypeA_in(st):
    st = normalize_code(st)
    grades = ["120m","60m","30m","15m"]
    for grade in grades:
        try:
            rst = F_MACD_TypeA(st,grade)
            # print(rst)
        except Exception as e:
            print("-------err %s %s %s"%(st,grade,e))
   

def F_MACD_TypeA(st,grade):
    # print("grade %s"% grade)
    df = libut.get_MACD(st,grade)
    if len(df.index) < 100:
        return -1
    # print(df[-20:])
    idxA = GetPointA(df)
    if idxA == -1:
        return -2
    #点A OK
    idxB = GetPointB(df,idxA)
    if idxB == -1:
        return -3
    # print("A:%s B:%s"%(df.loc[idxA,'time'],df.loc[idxB,'time']))
    if idxA - idxB > 50: #A点和B点相距太远的。算了
        return -4
    return CheckAB(st,grade,df,idxB,idxA)

# 检查AB两点是否满足要求
def CheckAB(st,grade,df,idxB,idxA):
    PA = df.loc[idxA,'close']
    PB = df.loc[idxB,'close']
    MD_A = df.loc[idxA,'macd']
    MD_B = df.loc[idxB,'macd']

    if (PA > PB) or MD_A < MD_B:
        return -5
    
    if (PB-PA)/PA*100 < 2.0: #AB差 新低/新高要明显
        return -6
    
    # Dif_A = df.loc[idxA,'dif']
    # Dif_B = df.loc[idxB,'dif']
    # if Dif_B >= Dif_A:
    #     return -7
    Dif_A = df.loc[idxA,'dea']
    Dif_B = df.loc[idxB,'dea']
    if Dif_B >= Dif_A:
        return -7
    
    prcNow = libut.GetPrcNow(st)
    rate = (PB - prcNow)/PB*100
    # if rate > 2:
    #     return -8
    print("---------result %s %s"%(st,grade))
    print("PointB  %s"%(df.loc[idxB,'time']))
    print("PointA  %s"%(df.loc[idxA,'time']))
    print('profit space:%.2f' % rate)
    # if (len(df.index)-idxA)<3:
    #     print("---- fresh %d X %s"%((len(df.index)-idxA),grade))
    # elif (len(df.index)-idxA)<6:
    #     print("-- fresh %d X %s ----"%((len(df.index)-idxA),grade))
    return True



def GetPointB(df,idxA):
    indexNow = idxA
    firstRedCnt = 0  #怕A是个超大绿
    while (indexNow > 0):
        vmacd = df.loc[indexNow,'macd'] 
        if vmacd > 0:
            break
        indexNow -= 1
        firstRedCnt += 1
    if firstRedCnt > 15:
        return -1  #放弃找B
        
    # 此时idx一定是红的
    # 找9绿
    GMAX = 9
    while (indexNow > 0):
        indexNow -= 1
        vmacd = df.loc[indexNow,'macd'] 
        if vmacd > 0:
            continue
        greenCnt = 1
        while(greenCnt < GMAX):
            indexNow -= 1
            vmacd = df.loc[indexNow,'macd'] 
            if vmacd > 0:
                greenCnt = 0
                break
            greenCnt += 1
            # print(df.irow(indexNow))
            #,df.loc[indexNow,'time'],greenCnt,vmacd
        if greenCnt != 0:
            # print("10个哦"+ str(indexNow))
            break
    dfB9 = df[indexNow:indexNow+GMAX+1]
    idxB = dfB9['close'].idxmin()
    
    # print(df.loc[idxB,'time'])
    
    # 因为close最小值可能是背离形式，一个MACD值突然变小的点。
    # 我们要的是MACD最绿块的那个点。是否要向左挪动？
    while(True):
        dfB3 = df[idxB-2:idxB+1]  #最近3条最小,够了。
        testIdx = dfB3['macd'].idxmin()
        # print("本次m值最小：%s"% df.loc[testIdx,'time'])
        if testIdx != idxB:
            idxB = testIdx
        else:
            break
        # vmacd1,vmacd0 = df.loc[idxB,'macd'],df.loc[idxB-1,'macd']
        # close1,close0 = df.loc[idxB,'close'],df.loc[idxB-1,'close']
        # if(vmacd0<=vmacd1 and close0<=close1):
            # idxB -= 1

    # print("Final",idxB,df.loc[idxB,'time'])
    return idxB
    

def GetPointA(df):
    df15 = df[-16:]
    idx15 = df15['close'].idxmin()
    df7 = df15[-8:]
    idx7 = df7['close'].idxmin()
    if idx7 == idx15:
        return idx7
    return -1



    
#最近的即时价格
def GetPrcNow(st):
    today = libut.GetToday()
    rst = get_price(st, end_date=today,count=1,skip_paused=False)
    NowPrc = rst['close'][0] #此时的价格
    return NowPrc
    
    
