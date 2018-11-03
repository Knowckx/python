import pandas as pd

def PDReadExcel(fPath):
    fPath = 'Quant/util/test.xlsx'
    with pd.ExcelFile(fPath) as xlsF:
        aa =xlsF.sheet_names
        print(aa)
        #显示出读入excel文件中的表名字
        # table1=xls_file.parse('first_sheet')
        # table2=xls_file.parse('second_sheet')

        # data1 = pd.read_excel(xlsF)
        # print(data1)


def PDWriteExcel(df,fPath):
        df_out.to_excel('tmp.xlsx',sheet_name='data')

        EW = pandas.ExcelWriter(fileName)
        df1.to_excel(EW)    #df1是一个DataFrame结构的数据
        EW.save()

if __name__ == '__main__':
        ExcelTest()
