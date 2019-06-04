# 初始化函数，设定基准等等
def initialize(context):
    today = libut.GetToday()
    st = normalize_code("000001.XSHG")
    stLen = 180
    df = get_price(st, end_date=today, frequency='daily', fields=['close'], skip_paused=True,count=stLen)
    df = df.reset_index()
    df.rename(columns={'index':'time'}, inplace = True)
    print(df)
    
    




def SaveToFile(filename = "df"):
    filename = filename+'.csv'
    write_file(filename, df.to_csv(), append=False) #写到文件中