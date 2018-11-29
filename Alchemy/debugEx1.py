# 把字符串（旧的excel写入）改成数组形式

#字符串 返回list
def HandleStr(prc):
    ss = str(prc).split("],")
    NL =str(ss[5]).split("[[")
    ss[5] = NL[0]
    ss.insert(6,NL[1])
    for i  in range(0,len(ss)):
        # print(i,ss[i])
        ss[i]= ss[i].replace("[","")
        ss[i] = ss[i].replace("]","")
        ss[i] = ss[i].replace(" ","")
    ss[5] = ss[5].replace(",","")
    # for i  in range(0,len(ss)):
    #     print(i,ss[i])
    return ss

def SetNL(NL,row):
    i = 0
    for pri in NL:
        i = i+1
        sht.Cells(row, 1+i).Value = pri

def main():
    global sht
    sht = ex.InitExcelSht()
    i = 110
    while True:
        i = i + 1
        print(i)
        prc = sht.Cells(i, 2).Value
        vv = str(prc)
        print(prc)
        if prc == None or prc == "":
            break
        if prc == "BookList":
            continue
        if vv.find("[") > -1:
            NL = HandleStr(prc)
            SetNL(NL,i)
    return
