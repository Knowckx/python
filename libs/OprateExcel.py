import win32com.client

#----------操作Excel表
def GetExcelSht(index=0):
    o = win32com.client.Dispatch("Excel.Application") #抓到Excel进程
    o.Visible = 1
    sht = o.Worksheets[index]
    return sht

def findCol(tar =""):
    for i in range(1,100):
        if sht.Cells(1,i).Value == tar:
            return i
    print("can't find target col")
    return -1
    	
def LoopCol(colI=1):
    i=0
    while True:
        i = i + 1
        prc = sht.Cells(i,colI).Value
        print(i,prc)
        if prc == None or prc == "":
            break
    return



def test():
    priceSet = ([1, 2, 3])
    # print(priceSet[1] = 10)
    print(priceSet)
    
#----------主程序
# ExcelMain()
# test()









#Workbooks.Open 打开
#Workbooks.Add()  #新增 返回一个Workbook
##.SaveAs(name) 保存
##.Save
##.Close
##sht = self.xlBook.Worksheets(sheet) 
##
##
##sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value  区域


##from win32com.client import Dispatch 
##import win32com.client 
##class easyExcel: 
##    """A utility to make it easier to get at Excel.  Remembering 
##    to save the data is your problem, as is  error handling. 
##    Operates on one workbook at a time.""" 
##    def __init__(self, filename=None): 
##        self.xlApp = win32com.client.Dispatch('Excel.Application') 
##        if filename: 
##            self.filename = filename 
##            self.xlBook = self.xlApp.Workbooks.Open(filename) 
##        else: 
##            self.xlBook = self.xlApp.Workbooks.Add() 
##            self.filename = ''  
##    def save(self, newfilename=None): 
##        if newfilename: 
##            self.filename = newfilename 
##            self.xlBook.SaveAs(newfilename) 
##        else: 
##            self.xlBook.Save()    
##    def close(self): 
##        self.xlBook.Close(SaveChanges=0) 
##        del self.xlApp 
##    def getCell(self, sheet, row, col): 
##        "Get value of one cell" 
##        sht = self.xlBook.Worksheets(sheet) 
##        return sht.Cells(row, col).Value 
##    def setCell(self, sheet, row, col, value): 
##        "set value of one cell" 
##        sht = self.xlBook.Worksheets(sheet) 
##        sht.Cells(row, col).Value = value 
##    def getRange(self, sheet, row1, col1, row2, col2): 
##        "return a 2d array (i.e. tuple of tuples)" 
##        sht = self.xlBook.Worksheets(sheet) 
##        return sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value 
##    def addPicture(self, sheet, pictureName, Left, Top, Width, Height): 
##        "Insert a picture in sheet" 
##        sht = self.xlBook.Worksheets(sheet) 
##        sht.Shapes.AddPicture(pictureName, 1, 1, Left, Top, Width, Height) 
##    def cpSheet(self, before): 
##        "copy sheet" 
##        shts = self.xlBook.Worksheets 
##        shts(1).Copy(None,shts(1)) 

