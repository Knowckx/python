import libs.Win32Excel as ex


def loopforDiv():
    i = 0
    while True:
        i = i + 1
        print(i)
        prc = sht.Cells(i,4).Value
        print(prc)
        if prc == None or prc == "":
            break
        
        if str(prc).find("[") >-1 or prc == "BookList":
            sht.Cells(i,10).Value = prc
            sht.Cells(i,4).Value = None
            print(prc)
        print(i,prc)
    return


def main():
    sht = ex.InitExcelSht()

    prc = sht.Cells(2,9).Value
    print(prc)
    prc = sht.Cells(2,11).Value
    print(prc)
    return

    i = 0
    while True:
        i = i + 1
        print(i)
        prc = sht.Cells(i,4).Value
        print(prc)
        if prc == None or prc == "":
            break
        
        if str(prc).find("[") >-1 or prc == "BookList":
            sht.Cells(i,10).Value = prc
            sht.Cells(i,4).Value = None
            print(prc)
        print(i,prc)
    return


main()