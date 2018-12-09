import libs.Win32Excel as ex
from bookut import extremum
sht = 1

# 找大小值
def analy():
    global sht
    sht = ex.InitExcelSht()
    coreCol = 7
    i = 0
    while True:
        i = i + 1
        prc = sht.Cells(i, 2).Value
        # print(i,prc)
        # if prc == None or prc == "" or i >= 1000:
        if prc == None or prc == "":
            break
        if prc == "BookList":
            i = i + 1
            vv = sht.Cells(i, coreCol).Value
            print(i,vv)
            extremum.PutNewV(vv,i)
    
    extremum.DumpHisty()



analy()

