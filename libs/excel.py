import pandas as pd




def ReadExcel():
    fPath = 'Quant/util/test.xlsx'
    with pd.ExcelFile(fPath) as xlsF:
        aa =xlsF.sheet_names
        print(aa)
        #显示出读入excel文件中的表名字
        # table1=xls_file.parse('first_sheet')
        # table2=xls_file.parse('second_sheet')

        # data1 = pd.read_excel(xlsF)
        # print(data1)

#excel文件和pandas的交互读写，主要使用到pandas中的两个函数,一个是pd.ExcelFile函数,一个是to_excel函数
def WriteExcel(df1,fileName):
    EW = pandas.ExcelWriter(fileName)
    df1.to_excel(EW)    #df1是一个DataFrame结构的数据
    EW.save()
    df_out.to_excel('tmp.xlsx')

def ExcelTest():
        df_out = pd.DataFrame([('string1', 1),
                ('string2', 2),
                ('string3', 3)],
                columns=['Name', 'Value'])
        print(df_out)
        df_out.to_excel('tmp.xlsx')
        # df1=pd.DataFrame({'Data1':[1,2,3,4,5,6,7]})
        # df2=pd.DataFrame({'Data2':[8,9,10,11,12,13]})
        # df3=pd.DataFrame({'Data3':[14,15,16,17,18]})
        # All=[df1,df2,df3]
        # fPath = 'Quant/util/test1.xlsx'
        # writer=pd.ExcelWriter(fPath, engine='xlsxwriter')
        # df1.to_excel(writer,sheet_name='data')
        # df2.to_excel(writer,sheet_name='data')
        # workbook = writer.book
        # worksheet = writer.sheets['data']
        # chart = workbook.add_chart({'type': 'column'})


if __name__ == '__main__':
        ExcelTest()
